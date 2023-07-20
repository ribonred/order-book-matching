import unittest
from main import Instrument, Order, OrderBook

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.instrument = Instrument(1, 'Instrument1', 100)
        self.order = Order(1, self.instrument.id, 2)
        self.order.total_price = self.instrument.price * self.order.quantity
        self.order_book = OrderBook()

    def test_add_order(self):
        self.order_book.add_order(self.order)
        self.assertIn(self.order, self.order_book.orders)

    def test_remove_order(self):
        self.order_book.add_order(self.order)
        self.order_book.remove_order(self.order.id)
        self.assertNotIn(self.order, self.order_book.orders)

    def test_get_total_value(self):
        self.order_book.add_order(self.order)
        expected_total_value = self.order.total_price
        self.assertEqual(self.order_book.get_total_value(), expected_total_value)

if __name__ == '__main__':
    unittest.main()
