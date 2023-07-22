from enum import Enum
from tabulate import tabulate
import locale
import socket
import pickle
import asyncio
import os
import time

locale.setlocale(locale.LC_ALL, "en_US")


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
        buy_orders = sorted(
            [
                order
                for order in self.orders
                if order.side == Side.BUY.value and order.status == "open"
            ],
            key=lambda order: order.price,
            reverse=True,
        )
        sell_orders = sorted(
            [
                order
                for order in self.orders
                if order.side == Side.SELL.value and order.status == "open"
            ],
            key=lambda order: order.price,
        )

        for buy_order in buy_orders:
            for sell_order in sell_orders:
                if (
                    sell_order.instrument == buy_order.instrument
                    and sell_order.price <= buy_order.price
                ):
                    match_quantity = min(buy_order.quantity, sell_order.quantity)
                    buy_order.quantity -= match_quantity
                    sell_order.quantity -= match_quantity
                    if buy_order.quantity == 0:
                        buy_order.status = "matched"
                    if sell_order.quantity == 0:
                        sell_order.status = "matched"
                    if buy_order.status == "matched":
                        break


class Exchange:
    def __init__(self):
        self.order_book: OrderBook = OrderBook()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get local machine name
        self._host = socket.gethostname()
        self._port = 9999

    def get_order(self, side: Side):
        return [
            order
            for order in self.order_book.orders
            if order.side == side and order.status == "open"
        ]

    def get_sell_order(self):
        return sorted(self.get_order(Side.SELL.value), key=lambda order: order.price)

    def get_buy_order(self):
        return sorted(
            self.get_order(Side.BUY.value), key=lambda order: order.price, reverse=True
        )

    async def order_handle(self, reader, writer):
        # First read the size of the data
        data: bytes = await reader.read()  # Assume the size is sent as a 4-byte integer
        order = pickle.loads(data)
        self.order_book.add_order(order)

    async def accept_order(self):
        self.server = await asyncio.start_server(
            self.order_handle, self._host, self._port
        )
        async with self.server:
            await self.server.serve_forever()

    def run(self):
        self._socket_loop = asyncio.new_event_loop()
        self._socket_loop.run_in_executor(
            None, self._socket_loop.run_until_complete, self.accept_order()
        )

    def print_book(self):
        buys = self.get_buy_order()
        sells = self.get_sell_order()
        table_book = tabulate({"buy": buys, "sell": sells}, headers="keys")
        print(table_book)

    def screen(self):
        self.run()
        try:
            while True:
                buys = self.get_buy_order()
                sells = self.get_sell_order()
                table_book = tabulate({"buy": buys, "sell": sells}, headers="keys")
                os.system("cls" if os.name == "nt" else "clear")  # Clear the console
                print(table_book)
                self.order_book.match_orders()
                time.sleep(1)
        except KeyboardInterrupt:
            self.server.close()

    def __add_order_socket(self, order: Order):
        # create a new socket
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connection to hostname on the port.
        _socket.connect((self._host, self._port))
        # serialize the object
        my_obj_bytes = pickle.dumps(order)
        # send the serialized object to the server
        _socket.sendall(my_obj_bytes)
        _socket.close()

    def add_order(self, order: Order, socket: bool = True):
        if socket:
            self.__add_order_socket(order)
        else:
            self.order_book.add_order(order)
