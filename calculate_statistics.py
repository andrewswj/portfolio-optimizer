import datetime

class CalculateStatistics:
    """
    Class which contains the functions we use to print as the output for the user.
    """
    def __init__(self, initial_aum, final_aum, b, e):
        self.initial_aum = initial_aum
        self.final_aum = final_aum
        #b and e need to be datetime objects
        self.start_date = b
        self.end_date = e
        self.n_days = (e - b).days

    def calculate_annual_return(self):
        return 365*(100*(self.final_aum - self.initial_aum)/self.initial_aum)/self.n_days
    
    def calculate_pnl(self):
        return self.final_aum - self.initial_aum
    
    def calculate_stock_return(self):
        return 100*(self.final_aum - self.initial_aum)/self.initial_aum
    
