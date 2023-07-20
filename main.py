class Instrument:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Order:
    def __init__(self, id, instrument_id, quantity, type):
        self.id = id
        self.instrument_id = instrument_id
        self.quantity = quantity
        self.type = type
        self.status = 'open'
        self.total_price = None

class OrderBook:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order_id):
        self.orders = [order for order in self.orders if order.id != order_id]

    def get_total_value(self):
        return sum(order.total_price for order in self.orders)
class Exchange:
    def __init__(self):
        self.order_book = []

    def add_order(self, order):
        self.order_book.append(order)

    def match_orders(self):
        for buy_order in [order for order in self.order_book if order.type == 'buy' and order.status == 'open']:
            for sell_order in [order for order in self.order_book if order.type == 'sell' and order.status == 'open' and order.instrument_id == buy_order.instrument_id]:
                if sell_order.quantity == buy_order.quantity:
                    buy_order.status = 'matched'
                    sell_order.status = 'matched'
                    break
