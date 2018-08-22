"""
Fetch all transactions from a specified base URL.

ASSUMPTIONS:

- the API returns a small number of transactions per page
    (i.e.: response size is bounded);

- the value of `totalCount` reported on every page does not change:
    let's pretend we are passing a parameter that allows the service to serve
    data from a snapshot of the database at a certain point in time;
    i.e.: all writes applied after such timestamp are not visible.
"""

import decimal
import json
import logging
from urllib2 import Request, urlopen, URLError

from .errors import UnexpectedResult
from .transaction import TransactionPage


# A typical result is less than 2k, so this is plenty:
MAX_RESULT_BUFFER_BYTES = 65536


class TransactionsFetcher(object):
    """
    Fetch all transactions from the specified URL.

    Result pages are translated to transaction entries, and then returned.
    """
    headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, base_url, fetch_timeout):
        self._base_url = base_url
        self._fetch_timeout = fetch_timeout

    def fetch_all(self):
        """Fetch all the pages containing transactions."""
        logging.info('Fetching all transactions...')

        page_number = 1
        first_page = self._fetch_page(page_number)
        for item in first_page.transactions:
            yield item

        # One possible performance improvement here is to add a pool of threads
        # (or coroutines) to fetch pages in parallel.
        # The content of the first page could be used to compute the expected
        # number of pages.
        # For now, we'll keep it simple and fetch one page at a time.

        num_transactions_to_fetch = (
            first_page.total_count - len(first_page.transactions)
        )
        while num_transactions_to_fetch > 0:
            logging.debug(
                '%d transactions to fetch', num_transactions_to_fetch
            )
            page_number += 1
            current_page = self._fetch_page(page_number)
            for item in current_page.transactions:
                yield item

            if current_page.total_count != first_page.total_count:
                # We need to contact the maintainers of the API and ask them
                # to fix this (or review our assumptions).
                raise UnexpectedResult(
                    "Total number of transactions has changed while fetching "
                    "pages (old: {}, new: {}). Please contact devs@bench.co"
                    .format(first_page.total_count, current_page.total_count)
                )
            num_transactions_to_fetch -= len(current_page.transactions)

        if num_transactions_to_fetch < 0:
            # We need to contact the maintainers of the API and ask them
            # to fix this.
            raise UnexpectedResult(
                "Total number of fetched transactions exceeds the expected "
                "value by {}. Please contact devs@bench.co"
                .format(abs(num_transactions_to_fetch))
            )

        logging.info('All transactions fetched.')

    def _fetch_page(self, page_number):
        """
        Fetch the specified page containing transactions.

        Raise urllib2.HTTPError if the result code is not 200.
        """
        # http://resttest.bench.co/transactions/{page_number}.json
        result = self._read_from_url(
            '{}{}.json'.format(self._base_url, page_number)
        )
        try:
            page_dict = json.loads(result)
            return TransactionPage.from_dict(page_dict)
        except (ValueError, decimal.InvalidOperation) as e:
            raise UnexpectedResult(
                "Cannot parse fetched transaction page. Reason: {}".format(e)
            )

    def _read_from_url(self, url):
        request = Request(url, headers=self.headers)
        try:
            result = _fetch(request, self._fetch_timeout)
        except (ValueError, URLError) as e:
            raise UnexpectedResult(
                "Cannot fetch document {}. Reason: {}".format(url, e)
            )
        if len(result) == MAX_RESULT_BUFFER_BYTES:
            # Something's wrong.
            # We need to review our assumptions.
            raise UnexpectedResult(
                "Response exceeds the expected max size. Please contact "
                "devs@bench.co"
            )
        return result


def _fetch(request, timeout):
    fd = urlopen(request, timeout=timeout)
    result = fd.read(MAX_RESULT_BUFFER_BYTES)
    fd.close()
    return result
