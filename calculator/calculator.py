"""Calculate balances from a list of transactions."""
from .aggregator import TransactionAggregator
from .fetcher import TransactionsFetcher


def calculate_balances(base_url, timeout):
    """Fetch transactions and print aggregated balances."""
    aggregator = TransactionAggregator()
    for transaction in TransactionsFetcher(base_url, timeout).fetch_all():
        aggregator.add(transaction)

    produce_reports(aggregator)


def produce_reports(aggregator):
    """Print aggregated balances."""
    # TODO: support multiple formats (e.g. HTML, Markdown, CSV, PDF, ...)
    print 'Daily balances:'
    for date, balance in aggregator.daily_balances:
        print date, balance

    print 'Total balance:'
    print aggregator.total_balance
