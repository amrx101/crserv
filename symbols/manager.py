import json
import requests
import logging
import sys

from symbols.model import Symbol


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
log.setLevel("DEBUG")


class SymbolManager(object):
    def __init__(self, file_path, symbol_url, currency_url):
        log.debug("Initializing Symbol Manager.")
        self.file_path = file_path
        self._symbol_url = symbol_url
        self._currency_url = currency_url
        self.symbols = list()
        self.full_names = dict()
        self.cache = dict()
        log.debug("Successfully initialized SymbolManager.")

    def start(self):
        log.debug("Starting SymbolManager Service.")
        self.gather_symbols()
        self.gather_full_name()
        self.create_symbols()
        log.debug("Successfully started SymbolManager Service.")

    def gather_symbols(self):
        symbols = requests.get(self._symbol_url)
        if symbols.status_code != 200:
            raise Exception("Unable to get symbols from server={}".format(symbols.status_code))

        symbols = symbols.json()
        currencies = dict()
        valids = set()
        for symbol in symbols:
            valids.add(symbol["id"])
            currencies[symbol["id"]] = (symbol["baseCurrency"], symbol["feeCurrency"])
        _symbols = list()
        with open(self.file_path) as f:
            _symbols = json.load(f)
        for symbol in _symbols:
            if symbol["symbol"] in valids:
                id = symbol["symbol"]
                self.symbols.append((id, currencies[id]))
            else:
               log.warn("Invalid symbol supplied={}".format(symbol))

        self.gather_full_name()

    def gather_full_name(self):
        currencies = requests.get(self._currency_url)
        if currencies.status_code != 200:
            raise Exception("Unable to gather currency info={}".format(currencies.status_code))
        currencies = currencies.json()
        for curr in currencies:
            self.full_names[curr["id"]] = curr["fullName"]

    def create_symbols(self):
        for sym, currency in self.symbols:
            id, fee_currency = currency
            full_name = self.full_names.get(id)
            symbol = Symbol(sym, id, fee_currency, full_name)
            self.cache[symbol.symbol] = symbol

    def get(self, symbol):
        if symbol not in self.cache:
            log.info("No entry for symbol={}".format(symbol))
            return None
        return self.cache.get(symbol).to_dict()

    def list(self):
        all_curr = []
        for v in self.cache.values():
            all_curr.append(v.to_dict())
        return all_curr

    def update(self, message):
        msg_dict = json.loads(message)
        if msg_dict.get("params"):
            values = msg_dict.get("params")
            symbol = values.get("symbol")
            if symbol in self.cache:
                self.cache[symbol].update(values)

    def get_symbols(self):
        return self.cache.keys()
