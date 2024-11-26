import pandas as pd
import numpy as np

def opening_range_strategy(data, rth_start='09:30', rth_end='15:59', window=5):
    """
    Apply a trading strategy based on the opening range breakout.
    :param data: DataFrame with OHLC and time data.
    :param rth_start: Start time of the regular trading hours (RTH).
    :param rth_end: End time of the regular trading hours (RTH).
    :param window: Opening range window in minutes.
    :return: DataFrame with a 'Signal' column indicating trades.
    """

    print(f"Arguments: {window}")

    # Convert rth_start and rth_end to time objects
    rth_start = pd.Timestamp(rth_start).time()
    rth_end = pd.Timestamp(rth_end).time()
    # Get end of opening range time
    rth_start_datetime = pd.Timestamp.combine(pd.Timestamp('today').date(), rth_start)
    orb_end = (rth_start_datetime + pd.Timedelta(minutes=window)).time()

    # Initialize Variables
    data['Signal'] = np.nan
    orb_high, orb_low = np.nan, np.nan
    HasTraded = False

    # Main Loop
    for idx, row in data.iterrows():

        current_time = row['Time']
        current_high = row['high']
        current_low = row['low']
        
        # Set ORB High and Low
        if current_time >= rth_start and current_time < orb_end:
            orb_high = max(orb_high, current_high) if not np.isnan(orb_high) else current_high
            orb_low = min(orb_low, current_low) if not np.isnan(orb_low) else current_low

        # Long or Short Entry, n minutes after RTH open
        if not HasTraded and current_time >= orb_end:
            current_close = row['close']
            if current_close > orb_high:
                data.at[idx, 'Signal'] = 1  # Buy Signal
                HasTraded = True
                # print('LONG')
            elif current_close < orb_low:
                data.at[idx, 'Signal'] = -1 
                HasTraded = True
                # print('SHORT')

        # Exit End of Day
        if current_time == rth_end:
            data.at[idx, 'Signal'] = 0  # Flatten position
            HasTraded = False
            orb_high = np.nan
            orb_low = np.nan
            # print('EOD')

    # Fill 'Signal' with the last valid value (carry-forward)
    data['Signal'] = data['Signal'].ffill()

    return data
