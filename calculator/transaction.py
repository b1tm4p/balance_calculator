"""Value objects used to model result pages and transactions."""
import datetime
import decimal
from .errors import InvalidPageFormat


class TransactionPage(object):
    """Immutable object containing a page worth of transactions."""
    def __init__(self, total_count, transactions):
        if not transactions:
            raise InvalidPageFormat(transactions)
        self._total_count = total_count
        self._transactions = transactions

    @property
    def total_count(self):
        return self._total_count

    @property
    def transactions(self):
        return self._transactions

    @classmethod
    def from_dict(cls, page_dict):
        """Convenient factory method."""
        try:
            return cls(
                total_count=int(page_dict['totalCount']),
                transactions=[
                    Transaction.from_dict(t)
                    for t in page_dict['transactions']
                ]
            )
        except (TypeError, KeyError):
            raise InvalidPageFormat(page_dict)


class Transaction(object):
    """Immutable object containing a transaction."""
    def __init__(self, date, amount):
        self._date = date
        self._amount = amount

    @property
    def date(self):
        return self._date

    @property
    def amount(self):
        return self._amount

    @classmethod
    def from_dict(cls, page_dict):
        """Convenient factory method."""
        return cls(
            date=datetime.datetime.strptime(
                page_dict['Date'], '%Y-%m-%d'
            ).date(),
            # using default precision (28 places):
            amount=decimal.Decimal(page_dict['Amount'])
        )
