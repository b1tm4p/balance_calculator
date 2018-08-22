#!/usr/bin/env python2

"""
Bench restTest.

This app:
- connects to a REST API;
- fetches all pages of financial transactions;
- calculates total balance and prints it to the console;
- calculates running daily balances and prints them to the console.

See http://resttest.bench.co/ for more details.
"""
import logging
import sys
from argparse import ArgumentParser
from .calculator import calculate_balances
from .errors import UnexpectedResult


DEFAULT_BASE_URL = 'http://resttest.bench.co/transactions/'
DEFAULT_FETCH_TIMEOUT_SEC = 5.0


def main():
    args = _get_args()
    _config_logging(args.verbose)
    try:
        calculate_balances(args.base_url, args.timeout)
    except UnexpectedResult as e:
        logging.error(e)
        raise SystemExit(1)

def _get_args():
    """Parse arguments passed to the command line."""
    parser = ArgumentParser(
        prog='calculator', description=(
            'Calculate running daily balances and the total balance for all '
            'financial transactions returned by `resttest.bench.co`.'
        )
    )
    # We may want to run our code against a different endpoint
    # (e.g. a DEV server):
    parser.add_argument(
        '--base-url', default=DEFAULT_BASE_URL, help='Base URL from which '
        'transactions must be fetched. Default: %(default)s'
    )
    parser.add_argument(
        '--timeout', type=float, default=DEFAULT_FETCH_TIMEOUT_SEC,
        help='Fetch timeout. Default: %(default)s'
    )
    parser.add_argument(
        '-v', '--verbose', action='count',
        help='Increase verbosity level at every occurrence.'
    )
    return parser.parse_args()


def _config_logging(verbose_count):
    index = max(verbose_count, 3)
    level = (
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    )[index]

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)-8s %(message)s',
        # TODO: log to syslog
        stream=sys.stdout,
        level=level
    )


main()
