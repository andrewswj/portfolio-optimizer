import numpy as np
import datetime

class CalculateStatistics:
    """
    Class which contains the functions we use to print as the output for the user.
    """
    def __init__(self, initial_aum, final_aum, b, e, daily_returns):
        self.initial_aum = initial_aum
        self.final_aum = final_aum
        #b and e need to be datetime objects
        self.start_date = b
        self.end_date = e
        self.n_days = (e - b).days
        self.daily_returns = daily_returns

    def calculate_annual_return(self):
        return 365*(100*(self.final_aum - self.initial_aum)/self.initial_aum)/self.n_days
    
    def calculate_pnl(self):
        return self.final_aum - self.initial_aum
    
    def calculate_stock_return(self):
        return 100*(self.final_aum - self.initial_aum)/self.initial_aum
    
    def calculate_annual_sharpe_ratio(self):
        daily_returns = np.array(self.daily_returns)
        annual_return = self.calculate_annual_return()
        annual_volatility = self.calculate_annual_volatility()
        risk_free_rate = 0.02  # Assuming a constant risk-free rate of 2%
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        return sharpe_ratio
    
    def calculate_annual_volatility(self):
        daily_returns = np.array(self.daily_returns)
        daily_volatility = np.std(daily_returns)
        annual_volatility = daily_volatility * np.sqrt(252)  # Assuming 252 trading days in a year
        return annual_volatility



if __name__ == '__main__':
    # Sample data
    initial_aum = 100000
    final_aum = 120000
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 31)
    daily_returns = [0.01, -0.005, 0.002, -0.008, 0.015, -0.01, 0.005]  # Just a sample, use actual daily returns

    # Create an instance of the CalculateStatistics class
    stats = CalculateStatistics(initial_aum, final_aum, start_date, end_date, daily_returns)

    # Calculate and print the statistics
    print("Annual Return:", stats.calculate_annual_return())
    print("PnL:", stats.calculate_pnl())
    print("Stock Return:", stats.calculate_stock_return())
    print("Annual Sharpe Ratio:", stats.calculate_annual_sharpe_ratio())
    print("Annual Volatility:", stats.calculate_annual_volatility())
