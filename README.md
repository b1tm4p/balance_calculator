# Balance calculator
Simple program to calculate balances from a list of transactions.

This app:
- connects to a REST API;
- fetches all pages of financial transactions;
- calculates total balance and prints it to the console;
- calculates running daily balances and prints them to the console.

See [resttest.bench.co](http://resttest.bench.co/) for more details.

## Prerequisites

You'll need python 2.7 to run this program.
In order to run the tests, you'll also need to install `python-pytest` and
`python-mock`.

## Installing

Just make a copy of this repo:

```sh
git clone https://github.com/b1tm4p/balance_calculator
```

## Running the program

Once you have downloaded the project folder, execute the following commands:

```sh
cd ./balance_calculator/

python2 -m calculator -vvv
```

You can see the list of accepted arguments by running:
```sh
python2 -m calculator -h
```
```
usage: calculator [-h] [--base-url BASE_URL] [--timeout TIMEOUT] [-v]

Calculate running daily balances and the total balance for all financial
transactions returned by `resttest.bench.co`.

optional arguments:
  -h, --help           show this help message and exit
  --base-url BASE_URL  Base URL from which transactions must be fetched.
                       Default: http://resttest.bench.co/transactions/
  --timeout TIMEOUT    Fetch timeout. Default: 5
  -v, --verbose        Increase verbosity level at every occurrence.
```

## Running the tests

You can run the suite of unit tests by executing:
```sh
py.test -v tests/
```
