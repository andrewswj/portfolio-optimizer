from weights import GetWeights
from getdata import Getdata
from parse_args import Parseargs
from calculate_statistics import CalculateStatistics
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class Optimize:
    """
    Main file to run. Optimizes a portfolio based on a given optimization strategy. 
    Parses arguments and queries yfinance once to calculate portfolio weights and final AUM
    given the strategy provided.
    """
    def __init__(self):
        #Parse arguments into a list
        self.list_arguments = Parseargs().parse_arguments()

        self.all_tickers = self.list_arguments[0]
        self.beginning_date = datetime.datetime.strptime(self.list_arguments[1], '%Y%m%d')
        self.end_date = self.list_arguments[2]
        #Get the adjusted beginning date so we can definitely get data for the period. 
        #500 days is just a rough measure.
        self.adj_beginning_date = datetime.datetime.strftime(self.beginning_date - datetime.timedelta(days=500), '%Y%m%d')

        #Get the dataframe of prices of all tickers for the entire period we'll need.
        getdata = Getdata(start_date = self.adj_beginning_date,
                                end_date = self.end_date,
                                ticker = self.list_arguments[0])

        self.full_prices_df =  getdata.data['Close']

        #Get end of month dates in our date range
        monthly_last_dates = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in getdata.buy_sell_dates()]
        start_date_boundary = datetime.datetime.strftime(self.beginning_date, '%Y-%m-%d')
        #Calculate dates to buy and sell on
        self.buy_sell_dates = [x for x in monthly_last_dates if x >= start_date_boundary]

        #Count back 250 trading days worth of data.
        self.num_days_lookback = 250
    
    def run_optimization_strategy(self):
        """
        Runs an optimization strategy (e.g. MV) provided by the user for the period.
        Lookback period = 250 trading days
        Buy sell dates are at the end of each month

        Returns: 

        aum (Final AUM after running the strategy over the period),
        overall_weights_df (Dataframe containing the weights for each stock each month for plotting)
        """
        #Initialize portfolio composition and AUM
        portfolio_composition = dict.fromkeys(self.all_tickers, 0)
        aum = self.list_arguments[3] #Initial AUM
        overall_weights_df = pd.DataFrame(columns = self.all_tickers)

        aum_list = [aum]
        for i in range(len(self.buy_sell_dates)):
            buy_date = self.buy_sell_dates[i]
            #Get the buy prices at the buy date
            buy_prices = self.full_prices_df.loc[buy_date,:]
            if i != 0: #If we're not at the start date
                aum = 0
                for pair in portfolio_composition.items():
                    #Recalculate the money we have at the end of the month for share purchases.
                    ticker = pair[0]
                    shares = pair[1]
                    sell_price = buy_prices.loc[ticker]
                    aum += sell_price * shares
                aum_list.append(aum)

            #Slice the data frame to get the past 250 trading days of data for the month.
            optimization_data_df = self.full_prices_df.loc[:buy_date][-self.num_days_lookback:]

            #Get the weights for the month according to the data
            if self.list_arguments[4] == 'msr':
                weights = GetWeights(optimization_data_df).max_sharpe_weights()
                weights_df = pd.DataFrame(weights, index = [i])
            
            elif self.list_arguments[4] == 'mv':
                weights = GetWeights(optimization_data_df).min_variance_weights()
                weights_df = pd.DataFrame(weights, index = [i])

            else:
                weights = GetWeights(optimization_data_df).hrp_weights()
                weights_df = pd.DataFrame(weights, index = [i])
            
            #Get a dataframe showing overeall weights
            overall_weights_df = pd.concat([overall_weights_df,weights_df])
            #Get the ticker names and weights accordingly
            ticker_names = list(weights)
            ticker_weights = list(weights.values())

            #Rebalance the portfolio
            for i in range(len(ticker_names)):
                money_to_buy_ticker = aum * ticker_weights[i]
                shares_bought = money_to_buy_ticker/(buy_prices.loc[ticker_names[i]])
                portfolio_composition[ticker_names[i]] = shares_bought
        
        overall_weights_df['dates'] = self.buy_sell_dates
        return aum, overall_weights_df, aum_list
    
    def plot_weights(self, df):
        """
        Plots the weights of each stock given a dataframe containing the weights for each stock.

        Returns:
        Plots a line graph via MatPlotLib.
        """
        if self.list_arguments[5]:#False if the user entered --plot_weights, True otherwise
            df.plot(x = 'dates', y = list(weights_df)[:-1])
            return plt.show()
        
    def calculate_daily_returns(self):
        return np.log(self.full_prices_df / self.full_prices_df.shift(1))

    
    def calculate_data(self, final_aum) -> None:
        daily_returns = self.calculate_daily_returns()
        
        calculator = CalculateStatistics(initial_aum=self.list_arguments[3],
                                        final_aum=final_aum,
                                        b=self.beginning_date,
                                        e=datetime.datetime.strptime(self.list_arguments[2], '%Y%m%d'),
                                        daily_returns=daily_returns)
        
        print('Annual Return (%):', calculator.calculate_annual_return())
        print('Profit and Loss ($):', calculator.calculate_pnl())
        print('Stock Return (%):', calculator.calculate_stock_return())
if __name__ == '__main__':
    optimizer = Optimize()
    strategy_results = optimizer.run_optimization_strategy()
    weights_df = strategy_results[1]
    monthly_aums_list = strategy_results[2]
    optimizer.plot_weights(weights_df)
    optimizer.calculate_data(final_aum = strategy_results[0])
