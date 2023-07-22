import uuid
import random
from main import Exchange, Instrument, Order, Side

BTC = Instrument("1", "BitCoin")

sides = [Side.BUY, Side.SELL]
ex = Exchange()

for _ in range(100):
    side = sides[random.randint(0, 1)]
    qty = random.randint(1, 15)
    price = random.randrange(1000, 1100)
    order = Order(uuid.uuid4().hex, BTC, side=side, quantity=qty, price=price)
    ex.add_order(order, socket=False)
ex.print_book()
ex.order_book.match_orders()
ex.print_book()

