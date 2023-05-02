from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import HRPOpt
from getdata import Getdata


class GetWeights:
    """
    Class which allows us to find the weights to use to purchase stocks,
    depending on the strategy.
    
    max_sharpe_weights returns the weights for max Sharpe Ratio.
    min_variance_weights when we use minimum volatility.
    hrp_weights returns the weights when we use HRP.
    """
    def __init__(self, df):
        self.prices_df = df

        #Get the expected returns for each stock and the sample covariance matrix 
        mu = expected_returns.mean_historical_return(self.prices_df)
        S = risk_models.sample_cov(self.prices_df)

        #Create the efficient frontier based on the historical data
        self.ef = EfficientFrontier(mu, S)

    def max_sharpe_weights(self):
        """
        Uses the Efficient Frontier to find the weights for the stocks in our universe
        based on maximizing the Sharpe Ratio. 

        Returns: An Ordered Dictionary of the weights.
        """
        #Need to calculate raw weights first
        raw_weights = self.ef.max_sharpe() 
        #Clean the weights
        cleaned_weights = self.ef.clean_weights()
        return cleaned_weights
    
    def min_variance_weights(self):
        """
        Uses the Efficient Frontier to find the weights for the stocks in our universe
        based on minimizing variance.

        Returns: An Ordered Dictionary of the weights.
        """
        #Need to calculate raw weights first
        raw_weights = self.ef.min_volatility() 
        #Clean the weights
        cleaned_weights = self.ef.clean_weights()
        return cleaned_weights
    
    def hrp_weights(self):
        """
        Uses a dataframe of prices to find the weights for the stocks in our universe
        based on hierarchal weight parity.

        Returns: An Ordered Dictionary of the weights.
        """
        rets = expected_returns.returns_from_prices(self.prices_df)
        hrp = HRPOpt(rets)
        hrp.optimize()
        cleaned_weights = hrp.clean_weights()
        return cleaned_weights
    
if __name__ == '__main__':
    print('Max Sharpe Ratio Weights:', GetWeights().max_sharpe_weights())
    print('Min Volatility Weights:', GetWeights().min_variance_weights())
    print('Hierarchal Risk Parity Weights:', GetWeights().hrp_weights())