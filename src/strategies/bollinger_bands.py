from .indicators.bollinger_bands import bollinger_bands

def bollinger_bands_strategy(data, window=20, num_std_dev=2):
    """
    Bollinger Bands strategy.
    """
    # Calculate Bollinger Bands
    data = bollinger_bands(data, window, num_std_dev)
    
    data['Signal'] = 0
    data.loc[data['close'] < data['Lower_Band'], 'Signal'] = 1
    data.loc[data['close'] > data['Upper_Band'], 'Signal'] = -1
    
    return data
