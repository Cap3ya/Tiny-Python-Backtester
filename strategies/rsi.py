from .indicators.rsi import rsi

def rsi_strategy(data, window=14, overbought=70, oversold=30):
    """
    RSI strategy.
    """
    # Calculate RSI
    data = rsi(data, window)
    
    data['Signal'] = 0
    data.loc[data['RSI'] < oversold, 'Signal'] = 1
    data.loc[data['RSI'] > overbought, 'Signal'] = -1
    
    return data
