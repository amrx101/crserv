import json
import requests


class SymbolManager(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.symbols = list()
        self.full_names = dict()
        self.cache = dict()
        self.gather_symbols()

    def gather_symbols(self):
        symbols = requests.get("https://api.hitbtc.com/api/2/public/symbol")
        if symbols.status_code != 200:
            raise Exception("Unable to get symbols from server")

        symbols = symbols.json()
        base_currency = dict()
        valids = set()
        for symbol in symbols:
            valids.add(symbol["id"])
            base_currency[symbol["id"]] = symbol["baseCurrency"]
        _symbols = list()
        with open(self.file_path) as f:
            _symbols = json.load(f)
        for symbol in _symbols:
            if symbol["symbol"] in valids:
                print symbol
                self.symbols.append(symbol)
            else:
                print("Not a valid symbol")

        self.gather_full_name()
        print self.symbols
        print self.full_names

    def validate_symbols(self):
        pass

    def gather_full_name(self):
        currencies = requests.get("https://api.hitbtc.com/api/2/public/currency")
        if currencies.status_code != 200:
            raise Exception("Unable to gather currency info={}", currencies.status_code)
        currencies = currencies.json()
        for curr in currencies:
            self.full_names[curr["id"]] = curr["fullName"]

    def get(self, symbol):
        pass

    def list(self):
        pass