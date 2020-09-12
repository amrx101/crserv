class Symbol(object):
    def __init__(self, symbol, id, fee_currency, full_name):
        self.symbol = symbol
        self.id = id
        self.fee_currency = fee_currency
        self.full_name = full_name
        self._ask = None
        self._bid = None
        self._last = None
        self._open = None
        self._low = None
        self._high = None

    @property
    def ask(self):
        return self.ask

    @ask.setter
    def ask(self, ask):
        self._ask = ask

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, bid):
        self._bid = bid

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, last):
        self._last = last

    @property
    def open(self):
        return  self._open

    @open.setter
    def open(self, open):
        self._open = open

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, low):
        self._low = low

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, high):
        self._high = high

    def to_dict(self):
        return dict(
            id=self.id,
            fullName=self.full_name,
            ask=self.ask,
            bid=self.bid,
            last=self.last,
            open=self.open,
            low=self.low,
            high=self.high,
            fee_currency=self.fee_currency
        )

    def update(self, params):
        for key, value in params.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
