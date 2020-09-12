from updater import Receiver
from flask import Flask
from symbols import SymbolManager

import tornado.ioloop
import tornado.web
import json
import time
import argparse



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


class HealthCheckHandler(JSONRequestHandler):
    def initialize(self):
        pass

    def get(self, *args, **kwargs):
        value = dict(message="AllOk")
        self.write_json(value)


class Application(object):
    def __init__(self, port, config, url_file):
        self._symbol_manager = None
        self._poller = None
        self._port = port
        self._urls = None
        self._initialize_services(config, url_file)

    def start(self):
        self.start_services()

    def stop(self):
        self._poller.stop()
        self._poller.join()
        tornado.ioloop.IOLoop.instance().stop()

    def _make_app(self):
        return tornado.web.Application([
            (r"/currency/[a-zA-Z0-9]+$", JSONRequestHandler, dict(symbol_manager=self._symbol_manager)),
            (r"/healthcheck", HealthCheckHandler)
        ])

    def _initialize_services(self, config, url_file):
        self.load_urls(url_file)
        self._symbol_manager = SymbolManager(
            config, self._urls.get("symbol"), self._urls.get("currency")
        )
        self._poller = Receiver(self._symbol_manager, self._urls.get("notifier"))
        self._app = self._make_app()
        self._app.listen(self._port)

    def load_urls(self, url_file):
        with open(url_file, "r") as f:
            self._urls = json.load(f)

    def start_services(self):
        self._poller.start()
        time.sleep(5)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except (Exception, KeyboardInterrupt, SystemExit):
            self.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help="port", default=5000, dest="port", type=int)
    parser.add_argument(
        '-c', help="config_file containing symbols",
        default="/etc/symbols.json", dest="config", type=str
    )
    parser.add_argument("-u", help="File containing URLS", default="/etc/urls.json", dest="urls", type=str)
    args = parser.parse_args()
    app = Application(args.port, args.config, args.urls)
    app.start()

