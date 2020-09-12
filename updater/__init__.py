import websocket
import ssl
import json
import time
import threading
import logging
import sys


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
log.setLevel("DEBUG")


class Receiver(threading.Thread):
    def __init__(self, symbol_manager, url):
        super(Receiver, self).__init__()
        self.url = url
        self.ws = websocket.WebSocketApp(
            self.url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.symbols = set()
        for symbol in symbol_manager.get_symbols():
            self.symbols.add(symbol)
        self.symbol_manager = symbol_manager

    def on_connect(self, *args, **kwargs):
        log.debug("Establish connection to server")

    def on_message(self, message):
        self.symbol_manager.update(message)

    def on_error(self, error):
        log.error("Error ={}, will attemp rerun".format(error))
        self._run()

    def on_open(self):
        messages = self.create_message()
        for pair in self.symbols:
            try:
                params = dict(symbol=pair)
                messages["params"] = params
                self.ws.send(json.dumps(messages))
                time.sleep(0.5)
            except Exception as e:
                log.warn(e)

    def create_message(self):
        message = dict()
        message["method"] = "subscribeTicker"
        message["id"] = 1
        return message

    # def _start(self):

    def run(self):
        log.debug("Starting Receiver service.")
        self._run()

    def _run(self):
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_close(self):
        log.debug("Closing the connection")

    def add_symbol(self, symbol):
        self.symbols.add(symbol)
        try:
            self.ws.send(symbol)
        except Exception as e:
            log.error("error while subscribing for symbol={}".format(e.message))

    def stop(self):
        log.debug("Shutting Down Receiver service.")
        self.ws.close()
