from Algorithm import Algorithm
from Portfolio import Portfolio
import numpy as np
from OrderApi import OrderApi
import logging

class Controller: 

    def __init__(self, portfolio = None, algorithm = None):
        self._logger = logging.getLogger(__name__)
        self._portfolio = Portfolio() if portfolio is None else portfolio
        self._algorithm = Algorithm() if algorithm is None else algorithm
        self._order_api = OrderApi()

    def backtest(cls, queue, controller = None):
        controller = cls() if controller is None else controller
        try:
            while True:
                if not queue.empty():
                    o = queue.get()
                    controller._logger.debug(o)

                    
                    if o == 'POISON':
                        # Poison Pill!
                        break

                    timestamp = o[0]
                    ticker = o[1]
                    price = o[2]

                    # Update pricing
                    controller.process_pricing(ticker = ticker, price = price)

                    # Generate Orders
                    orders = controller._algorithm \
                            .generate_orders(timestamp, controller._portfolio)

                    # Process orders
                    if len(orders) > 0:
                        # Randomize the order execution
                        final_orders = [orders[k] for k in np.random.choice(len(orders), 
                                                                            replace=False, 
                                                                            size=len(orders))]

                        for order in final_orders:
                            controller.process_order(order)

                        controller._logger.info(controller._portfolio.value_summary(timestamp))

        except Exception as e:
            print(e)
        finally:
            controller._logger.info(controller._portfolio.value_summary(None))

    def process_order(self, order):
        success = False
        receipt = self._order_api.process_order(order)
        if receipt is not None:
            success = self.process_receipt(receipt)

        if order is None or success is False:
            self._logger.info(('{order_type} failed: %s at $%s for %s shares' % order).format(order_type = 'Sell' if order[2] < 0 else 'Buy'))

    def process_receipt(self,receipt):
        ticker = receipt[0]
        price = receipt[1]
        share_delta = receipt[2]
        fee = receipt[3]
        temp = self._portfolio.balance - (price * share_delta + fee)
        if temp > 0:
            if share_delta < 0 and -share_delta > self._portfolio.get_shares(ticker):
                # Liquidate
                share_delta = -self._portfolio.get_shares(ticker)
                fee = self._order_api._calculate_fee(share_delta*price)
                if fee > abs(share_delta*price):
                    return False

            self._portfolio.update_trade(ticker=ticker, price=price, share_delta=share_delta, fee=fee)
            self._logger.debug('Trade on %s for %s shares at %s with fee %s' % (ticker,share_delta,price, fee))
            return True

        return False

    def process_pricing(self, ticker, price):
        self._portfolio.update(price=price, ticker = ticker)
        self._algorithm.update(stock=ticker, price = price)