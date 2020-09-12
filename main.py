from updater import Receiver
from flask import Flask
from symbols import SymbolManager

import tornado.ioloop
import tornado.web
import json
import time


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


class Application(object):
    def __init__(self):
        self._symbol_manager = None
        self._poller = None
        self._initialize_services()

    def start(self):
        self.start_services()

    def stop(self):
        self._poller.stop()
        self._poller.join()
        tornado.ioloop.IOLoop.instance().stop()

    def _make_app(self):
        return tornado.web.Application([
            (r"/currency/[a-zA-Z0-9]+$", JSONRequestHandler, dict(symbol_manager=self._symbol_manager)),
        ])

    def _initialize_services(self):
        self._symbol_manager = SymbolManager("/Users/amit/crserv/symbols.json")
        self._poller = Receiver(self._symbol_manager)
        self._app = self._make_app()
        self._app.listen(5000)

    def start_services(self):
        self._poller.start()
        time.sleep(5)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except (Exception, KeyboardInterrupt, SystemExit):
            self.stop()


if __name__ == "__main__":
    app = Application()
    app.start()

