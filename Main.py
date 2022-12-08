from multiprocessing import Process, Queue
import DataSource
import Controller
import logging
import datetime as dt


class Backtester:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._settings = {}

        self._default_settings = {
            'Portfolio' : Portfolio(),
            'Algorithm' : Algorithm(),
            'Source' : 'yahoo',
            'Start_Day' : dt.datetime(2016,1,1),
            'End_Day' : dt.datetime.today(),
            'Tickers' : ['AAPL','GOGL','MSFT','AA','APB']
        }

    def set_portfolio(self, portfolio):
        self._settings['Portfolio'] = portfolio

    def set_algorithm(self, algorithm):
        self._settings['Algorithm'] = algorithm

    def set_source(self, source):
        self._settings['Source'] = source

    def set_start_date(self, date):
        self._settings['Start_Day'] = date

    def set_end_date(self, date):
        self._settings['End_Day'] = date

    def set_stock_universe(self, stocks):
        self._settings['Tickers'] = stocks

    def get_setting(self, setting):
        return self._settings[setting] if setting in self._settings else self._default_settings[setting]

    def backtest(self):
        #Setup Logger
        root = logging.getLogger()
        root.setLevel(level=logging.DEBUG)
        import os
        filepath = 'run.log'
        if os.path.exists(filepath):
            os.remove(filepath)

        root.addHandler(logging.FileHandler(filename=filepath))

        # Initiate run
        q = Queue()
        ds = None
        c = None

        ds = DataSource(
            source=self.get_setting('Source'),
            start=self.get_setting('Start_Day'),
            end=self.get_setting('End_Day'),
            tickers=self.get_setting('Tickers')
        )
        c = Controller(
            portfolio=self.get_setting('Portfolio'),
            algorithm=self.get_setting('Algorithm')
        )

        p = Process(target=DataSource.process, args=((q,ds)))
        p1 = Process(target=Controller.backtest, args=((q,c)))

        p.start()
        p1.start()
        p.join()
        p1.join()


if __name__ == '__main__':
    b = Backtester()
    b.backtest()

