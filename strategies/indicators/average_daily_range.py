import pandas as pd

def average_daily_range(data, window=21):
    """
    Calculate the rolling average of the daily range (high - low) over the past 21 days 
    and add it as a new column to the minute-level data.
    """

    # Calculate the daily range (High - Low) for each day
    daily_ranges = data.groupby('Date').pipe(lambda x: x['high'].max() - x['low'].min())

    # Calculate the rolling average of the daily range over the past 21 days
    average_daily_range = daily_ranges.rolling(window=window, min_periods=1).mean()

    # Map the rolling average back to the minute-level data
    data['AverageDailyRange'] = data['Date'].map(average_daily_range)

    # Return the data with the added 'RollingAvgDailyRange' column
    return data
