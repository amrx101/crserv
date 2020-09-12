import websocket
import ssl
import json
import time
import threading
'''
wscat -c wss://api.hitbtc.com/api/2/ws

{
  "method": "subscribeTicker",
  "params": {
    "symbol": "ETHBTC"
  },
  "id": 123
}
'''


class Receiver(threading.Thread):
    def __init__(self, symbol_manager):
        super(Receiver, self).__init__()
        self.url = "wss://api.hitbtc.com/api/2/ws"
        self.ws = websocket.WebSocketApp(
            self.url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.symbols = set()
        for symbol in symbol_manager.get_symbols():
            self.symbols.add(symbol)
        self.symbol_manager = symbol_manager

    def on_connect(self, *args, **kwargs):
        print "connect"

    def on_message(self, message):
        self.symbol_manager.update(message)

    def on_error(self, error):
        print(error)

    def on_open(self):
        messages = self.create_message()
        for pair in self.symbols:
            try:
                params = dict(symbol=pair)
                messages["params"] = params
                self.ws.send(json.dumps(messages))
                time.sleep(1)
            except Exception as e:
                print(e)

    def create_message(self):
        message = dict()
        message["method"] = "subscribeTicker"
        message["id"] = 1
        return message

    # def _start(self):

    def run(self):
        self._run()

    def _run(self):
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_close(self):
        print "close"

    def add_symbol(self, symbol):
        self.symbols.add(symbol)
        try:
            self.ws.send(symbol)
        except Exception as e:
            print("error while subsribing for symbol={}".format(e.message))
