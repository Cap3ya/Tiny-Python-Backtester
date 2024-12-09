def moving_average(data, window=20):
    """
    Calculate simple moving average (SMA) for a given window.
    """
    data['SMA'] = data['close'].rolling(window=window).mean()
    return data
