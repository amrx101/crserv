from updater import Receiver
from flask import Flask
from symbols import SymbolManager

import tornado.ioloop
import tornado.web
import json


class JSONRequestHandler(tornado.web.RequestHandler):
    def initialize(self, symbol_manager):
        self.symbol_manager = symbol_manager

    def get(self):
        symbol = self.request.uri.split("/")[2]
        if symbol == "all":
            items = self.symbol_manager.list()
            self.write_json(items)
        else:
            value = self.symbol_manager.get(symbol)
            if not value:
                message = "Currency with symbol={} Does Not Exist".format(symbol)
                self.write_error(status_code=404, message=message)
                self.finish()
                return
            self.write(json.dumps(value))

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_json(self, value):
        self.write(json.dumps(value))

    def write_error(self, status_code, **kwargs):
        if "message" not in kwargs:
            if status_code == 405:
                kwargs["message"] = "Invalid HTTP method"
            else:
                kwargs["message"] = "Unknown Error"
        self.write_json(kwargs)


def make_app(symbol_manager):
    return tornado.web.Application([
        (r"/currency/[a-zA-Z]+$", JSONRequestHandler, dict(symbol_manager=symbol_manager)),
    ])


if __name__ == "__main__":
    print "Hello"
    symbols = ["BTCUSD", "ETHBTC"]
    s = SymbolManager("/Users/amit/crserv/symbols.json")
    r = Receiver(s)
    r.start()
    # print "comes here"
    app = make_app(s)
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
    # r.join()