from .indicators.moving_average import moving_average

def moving_average_crossover(data, short_window=20, long_window=50):
    """
    Moving Average Crossover strategy.
    """
    # Calculate short and long moving averages
    data = moving_average(data, short_window)
    data = moving_average(data, long_window)
    
    data['Signal'] = 0
    data.loc[data['SMA'] > data['SMA'].shift(), 'Signal'] = 1
    data.loc[data['SMA'] <= data['SMA'].shift(), 'Signal'] = -1
    
    return data
