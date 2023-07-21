from enum import Enum
from tabulate import tabulate
import locale

locale.setlocale(locale.LC_ALL, 'en_US')
class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Instrument:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Order:
    def __init__(
        self, id: str, instrument: Instrument, quantity: float, side: Side, price: float
    ):
        self.id = id
        self.instrument = instrument
        self.quantity = quantity
        self.side = side.value
        self.status = "open"
        self.price = price
    
    def __str__(self) -> str:
        return f"{self.quantity} @{locale.currency(self.price, grouping=True)}"


class OrderBook:
    def __init__(self):
        self.orders: list[Order] = []

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order_id):
        self.orders = [order for order in self.orders if order.id != order_id]

    def get_total_value(self):
        return sum(order.price for order in self.orders)

    def match_orders(self):
        for buy_order in [
            order
            for order in self.orders
            if order.side == Side.BUY.value and order.status == "open"
        ]:
            for sell_order in [
                order
                for order in self.orders
                if order.side == Side.SELL.value
                and order.status == "open"
                and order.instrument == buy_order.instrument
            ]:
                if sell_order.quantity == buy_order.quantity:
                    buy_order.status = "matched"
                    sell_order.status = "matched"
                    break


class Exchange:
    def __init__(self):
        self.order_book: OrderBook = OrderBook()

    def get_order(self, side: Side):
        return [
            order
            for order in self.order_book.orders
            if order.side == side and order.status == "open"
        ]

    def get_sell_order(self):
        return self.get_order(Side.SELL.value)
    
    def get_buy_order(self):
        return self.get_order(Side.BUY.value)
    
    def screen(self):
        buys = self.get_buy_order()
        sells = self.get_sell_order()
        table_book = tabulate(
            {
                "buy": buys,
                "sell": sells
            },
            headers="keys"
        )
        print(table_book)

    def add_order(self, order: Order):
        self.order_book.add_order(order)
