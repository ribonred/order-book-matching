import unittest
from main import Instrument, Order, OrderBook, Side

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.instrument = Instrument('1', 'Instrument1', 100)
        self.buy_order = Order('1', self.instrument, 2, Side.BUY)
        self.sell_order = Order('2', self.instrument, 2, Side.SELL)
        self.buy_order.total_price = self.instrument.price * self.buy_order.quantity
        self.sell_order.total_price = self.instrument.price * self.sell_order.quantity
        self.order_book = OrderBook()
        self.exchange = Exchange()

    def test_add_order(self):
        self.exchange.add_order(self.buy_order)
        self.assertIn(self.buy_order, self.exchange.order_book)

    def test_remove_order(self):
        self.exchange.add_order(self.buy_order)
        self.exchange.remove_order(self.buy_order.id)
        self.assertNotIn(self.buy_order, self.exchange.order_book)

    def test_get_total_value(self):
        self.exchange.add_order(self.buy_order)
        expected_total_value = self.buy_order.total_price
        self.assertEqual(self.exchange.get_total_value(), expected_total_value)

    def test_match_orders(self):
        self.exchange.add_order(self.buy_order)
        self.exchange.add_order(self.sell_order)
        self.exchange.match_orders()
        self.assertEqual(self.buy_order.status, 'matched')
        self.assertEqual(self.sell_order.status, 'matched')

if __name__ == '__main__':
    unittest.main()
