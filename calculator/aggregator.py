import datetime
from collections import defaultdict
from decimal import Decimal
from .transaction import Transaction


class TransactionAggregator(object):
    def __init__(self):
        # If the number of days grows so much that it no longer fits in RAM,
        # we'll have to replace this dictionary with an actual database.
        # That is unlikely though.
        self._db = defaultdict(Decimal)
        self._min_date = datetime.date(3000, 1, 1)
        self._max_date = datetime.date(1000, 1, 1)

    def add(self, transaction):
        assert isinstance(transaction, Transaction)
        self._db[transaction.date] += transaction.amount
        self._min_date = min(transaction.date, self._min_date)
        self._max_date = max(transaction.date, self._max_date)

    @property
    def daily_balances(self):
        current_date = self._min_date
        while current_date <= self._max_date:
            balance = self._db.get(current_date, Decimal(0))
            yield current_date, balance
            current_date += datetime.timedelta(days=1)

    @property
    def total_balance(self):
        return sum(amount for amount in self._db.itervalues())
