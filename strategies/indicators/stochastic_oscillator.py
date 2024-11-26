def stochastic_oscillator(data, window=14):
    """
    Calculate the Stochastic Oscillator.
    """
    data['Low_Min'] = data['Low'].rolling(window=window).min()
    data['High_Max'] = data['High'].rolling(window=window).max()
    data['Stochastic'] = 100 * (data['close'] - data['Low_Min']) / (data['High_Max'] - data['Low_Min'])
    return data
