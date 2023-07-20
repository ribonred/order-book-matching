from enum import Enum


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Instrument:
    def __init__(self, id: str, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price


class Order:
    def __init__(self, id: str, instrument: Instrument, quantity: float, side: Side):
        self.id = id
        self.instrument_id = instrument
        self.quantity = quantity
        self.side = side.value
        self.status = "open"
        self.total_price = None


class OrderBook:
    def __init__(self):
        self.orders : list[Order] = []

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order_id):
        self.orders = [order for order in self.orders if order.id != order_id]

    def get_total_value(self):
        return sum(order.total_price for order in self.orders)


class Exchange:
    def __init__(self):
        self.order_book: list[OrderBook] = []

    def add_order(self, order: OrderBook):
        self.order_book.append(order)

    def match_orders(self):
        for buy_order in [
            order
            for order in self.order_book
            if order.side == Side.BUY and order.status == "open"
        ]:
            for sell_order in [
                order
                for order in self.order_book
                if order.side == Side.SELL
                and order.status == "open"
                and order.instrument_id == buy_order.instrument_id
            ]:
                if sell_order.quantity == buy_order.quantity:
                    buy_order.status = "matched"
                    sell_order.status = "matched"
                    break
