# Balance calculator
Simple program to calculate balances from a list of transactions.

This app:
- connects to a REST API;
- fetches all pages of financial transactions;
- calculates total balance and prints it to the console;
- calculates running daily balances and prints them to the console.

See [resttest.bench.co](http://resttest.bench.co/) for more details.

You can run the program by executing the following commands:
```sh
git clone https://github.com/b1tm4p/balance_calculator

cd ./balance_calculator/

python2.7 calculate_balances.py
```

```
python2.7 calculate_balances.py -h

usage: calculate_balances.py [-h] [--base-url BASE_URL] [--timeout TIMEOUT]
                             [-v]

Calculate running daily balances and the total balance for all financial
transactions returned by `resttest.bench.co`.

optional arguments:
  -h, --help           show this help message and exit
  --base-url BASE_URL  Base URL from which transactions must be fetched.
                       Default: http://resttest.bench.co/transactions/
  --timeout TIMEOUT    Fetch timeout. Default: 5
  -v, --verbose        Increase verbosity level at every occurrence.
```
