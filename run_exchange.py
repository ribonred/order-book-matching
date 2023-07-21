from main import Instrument, Order, Exchange, Side
import uuid


BTC = Instrument("1", "BitCoin")

exchange = Exchange()
order1= Order(uuid.uuid4().hex, BTC,side=Side.BUY, quantity=3, price=12_000.5 )
order2= Order(uuid.uuid4().hex, BTC,side=Side.SELL, quantity=3, price=12_000.5 )

exchange.add_order(order1)
exchange.add_order(order2)

exchange.run()

