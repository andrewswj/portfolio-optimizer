import argparse
from args_check import ArgsCheck

class Parseargs:
    """
    A class which parses the arguments passed into a program.
    """
    def __init__(self):
        """
        Requires the following arguments:
        --tickers: Comma-separated list of tickers e.g. AAPL,MSFT,KO
        --b: Beginning date in YYYYMMDD format
        --e: End date in YYYYMMDD format
        --initial_aum: A number > 0. e.g. 1000
        --optimizer: msr/hrp/mv.
        --plot_weights: Indicates whether to plot weight or not.
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--tickers', type=str, help='comma-separated list of tickers')
        self.parser.add_argument('--b', type=str, help='start date in YYYYMMDD format')
        self.parser.add_argument('--e', type=str, help='end date in YYYYMMDD format')
        self.parser.add_argument('--initial_aum', type=float, help='initial assets under management')
        self.parser.add_argument('--optimizer', type=str, help='optimizer (msr/mv/hrp)')
        self.parser.add_argument('--plot_weights', action = 'store_true', help='whether to plot weights')


    def parse_arguments(self, arguments = None):
        """
        Parses arguments and returns a list where arguments are in the following index order:
        0: tickers
        1: beginning date
        2: end date
        3: initial aum
        4: optimizer
        5: plot_weights: True if user entered --plot_weights, False otherwise.
        """
        namespace_args = self.parser.parse_args(namespace = arguments)
        tickers = namespace_args.tickers.split(',')  # Split the comma-separated tickers string into a list
        list_arguments = [tickers, 
                          namespace_args.b, 
                          namespace_args.e, 
                          namespace_args.initial_aum, 
                          namespace_args.optimizer,
                          namespace_args.plot_weights
                          ]
        """
        Code below uses ArgsCheck from args_check.py
        to see if the arguments pass the tests.

        If the arguments do not pass the tests, an error message will be printed and the 
        program will exit.
        """
        ArgsCheck.ticker_check(list_arguments[0])
        ArgsCheck.date_check(list_arguments[1], list_arguments[2])
        ArgsCheck.aum_check(list_arguments[3])
        ArgsCheck.optimizer_check(list_arguments[4])
        return list_arguments
    
if __name__ == '__main__':
    x = Parseargs()
    print(x.parse_arguments())
