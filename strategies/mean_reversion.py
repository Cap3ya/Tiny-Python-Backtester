from .indicators.moving_average import moving_average

def mean_reversion_strategy(data, window=20):
    """
    Mean Reversion strategy using moving average.
    """
    # Calculate moving average
    data = moving_average(data, window)
    
    data['Signal'] = 0
    data.loc[data['close'] < data['SMA'], 'Signal'] = 1
    data.loc[data['close'] > data['SMA'], 'Signal'] = -1
    
    return data
