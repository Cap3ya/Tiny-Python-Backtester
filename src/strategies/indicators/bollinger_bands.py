def bollinger_bands(data, window=20, num_std_dev=2):
    """
    Calculate Bollinger Bands (Upper, Lower, and Middle).
    """
    data['SMA'] = data['close'].rolling(window=window).mean()
    data['Upper_Band'] = data['SMA'] + (data['close'].rolling(window=window).std() * num_std_dev)
    data['Lower_Band'] = data['SMA'] - (data['close'].rolling(window=window).std() * num_std_dev)
    return data
