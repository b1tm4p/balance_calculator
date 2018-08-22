from urllib2 import URLError, HTTPError
import glob
import mock
import os
import pytest
import socket

from calculator.errors import UnexpectedResult, InvalidPageFormat
from calculator.fetcher import TransactionsFetcher


def _raise_http_error(*a, **k):
    raise HTTPError('url', 404, 'Not Found', {}, None)


@pytest.mark.parametrize('raised_exception', [
    ValueError('unknown url type: <garbage>1.json'),
    URLError(socket.error(111, 'Connection refused')),
    URLError(socket.gaierror(-2, 'Name or service not known')),
    URLError(socket.timeout('timed out')),
    _raise_http_error,
])
def test_fetch_errors(raised_exception):
    """Simulate fetching errors."""
    tf = TransactionsFetcher('some_url', fetch_timeout=1.2)
    with mock.patch('calculator.fetcher._fetch', side_effect=raised_exception):
        with pytest.raises(UnexpectedResult):
            next(tf.fetch_all())


def test_fetch_valid_results():
    """
    Simulate success in fetching pages.

    The data is read from json files stored in the fixtures folder.
    """
    pages = glob.glob(
        os.path.join(
            os.path.dirname(__file__), 'fixtures', '*.json'
        )
    )

    def fetch(*a, **k):
        return open(pages.pop(0)).read()

    tf = TransactionsFetcher('some_url', fetch_timeout=1.2)
    with mock.patch('calculator.fetcher._fetch', side_effect=fetch):
        assert list(tf.fetch_all())


def test_fetch_invalid_json():
    tf = TransactionsFetcher('some_url', fetch_timeout=1.2)
    with mock.patch('calculator.fetcher._fetch', return_value='xxx'):
        with pytest.raises(UnexpectedResult) as excinfo:
            next(tf.fetch_all())
        assert 'No JSON object could be decoded' in str(excinfo.value)


@pytest.mark.parametrize('return_value', [
    '""',
    '[]',
    '{}',
    '[{}]',
    '[1]',
    '[{"1": 2}]',

    '''{
        "totalCount": 38,
        "transactions": []
    }''',

    '''{
        "transactions": [{
            "Date": "2013-12-22",
            "Amount": "-110.71"
        }]
    }''',

    '''{
        "totalCount": 38,
        "transactions": [{
            "Amount": "-110.71"
        }]
    }''',

    '''{
        "totalCount": 38,
        "transactions": [{
            "Amount": "-110.71"
        }]
    }''',
])
def test_fetch_invalid_response(return_value):
    tf = TransactionsFetcher('some_url', fetch_timeout=1.2)
    with mock.patch('calculator.fetcher._fetch', return_value=return_value):
        with pytest.raises(InvalidPageFormat) as excinfo:
            next(tf.fetch_all())
