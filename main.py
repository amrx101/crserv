from updater import Receiver
#
#
#
from symbols import SymbolManager
if __name__ == "__main__":
    print "Hello"
    # symbols = ["BTCUSD", "ETHBTC"]
    s = SymbolManager("/Users/amit/crserv/symbols.json")
    r = Receiver(s)
    r.start()