from calculator.aggregator import TransactionAggregator, Transaction


def test_no_transactions():
    aggregator = TransactionAggregator()
    assert list(aggregator.daily_balances) == []
    assert aggregator.total_balance == 0


def test_one_transaction():
    aggregator = TransactionAggregator()
    d = {
        'Date': '2018-08-21',
        'Amount': '-1936.27'
    }
    aggregator.add(
        Transaction.from_dict(d)
    )
    assert str(aggregator.total_balance) == d['Amount']

    daily_balances = list(aggregator.daily_balances)
    assert len(daily_balances) == 1
    date, amount = daily_balances[0]
    assert str(date) == d['Date']
    assert str(amount) == d['Amount']


def test_aggregation_by_date():
    aggregator = TransactionAggregator()
    d = {
        'Date': '2018-08-21',
        'Amount': '-10.01'
    }
    t = Transaction.from_dict(d)
    aggregator.add(t)
    aggregator.add(t)

    expected_amount = '-20.02'
    assert str(aggregator.total_balance) == expected_amount

    daily_balances = list(aggregator.daily_balances)
    assert len(daily_balances) == 1
    date, amount = daily_balances[0]
    assert str(date) == d['Date']
    assert str(amount) == expected_amount


def test_missing_date():
    aggregator = TransactionAggregator()
    aggregator.add(
        Transaction.from_dict({'Date': '2018-09-02', 'Amount': '1'})
    )
    aggregator.add(
        Transaction.from_dict({'Date': '2018-08-31', 'Amount': '1'})
    )

    assert aggregator.total_balance == 2

    daily_balances = list(aggregator.daily_balances)
    assert len(daily_balances) == 3

    # the missing date must have been automatically added
    date, amount = daily_balances[1]
    assert str(date) == '2018-09-01'
    assert amount == 0
