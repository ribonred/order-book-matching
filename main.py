class Instrument:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Order:
    def __init__(self, id, instrument_id, quantity):
        self.id = id
        self.instrument_id = instrument_id
        self.quantity = quantity
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
