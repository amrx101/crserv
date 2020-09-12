class Symbol(object):
    def __init__(self, symbol, id, base_currency, fee_currency, full_name):
        self.id = symbol
        self.id = id
        self.base_currency = base_currency
        self.fee_currency = fee_currency
        self.full_name = full_name
        self.ask = None
        self.bid = None
        self.last = None
        self.open = None
        self.low = None
        self.high = None

    def to_dict(self):
        return dict(
            id=self.base_currency,
            fullName=self.full_name,
            ask=self.ask,
            bid=self.bid,
            last=self.last,
            open=self.open,
            low=self.low,
            high=self.high,
            fee_currency=self.fee_currency
        )
