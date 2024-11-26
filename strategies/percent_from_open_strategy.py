import pandas as pd
import numpy as np

def percent_from_open_strategy(data, rth_start='09:30', rth_end='15:59', entry_multiplier=0.002, stop_multiplier=-0.005, limit_multiplier=0.04):
    # best parameters entry_multiplier=0.002, stop_multiplier=-0.005, limit_multiplier=0.04 Return: 1.73
    
    """
    Percent from Open Strategy:
    - Maximum 1 trade per day (either long or short).
    - Exit on limit, stop, or end of day.
    - Uses percentage to define entry, limit, and stop levels.
    - Works during RTH (9:30 AM to 4:00 PM).
    """
    print(f"Function arguments: {entry_multiplier, stop_multiplier, limit_multiplier}")
    
    # Convert rth_start and rth_end to time objects
    rth_start = pd.Timestamp(rth_start).time()
    rth_end = pd.Timestamp(rth_end).time()

    # Initialize trading variables and columns
    data['Signal'] = np.nan
    close_price = np.nan
    open_price = np.nan
    HasTraded = False
    isLong = False 
    isShort = False
    long_entry = np.nan
    short_entry = np.nan
    long_limit = np.nan
    short_limit = np.nan
    long_stop = np.nan
    short_stop = np.nan
    
    # Iterate over rows and calculate signals and manage trades
    for idx, row in data.iterrows():
        
        # Set RTH open price (at the start of the RTH period)
        if row['Time'] == rth_start:
            open_price = row['open']
            long_entry = open_price * (1 + entry_multiplier)
            short_entry = open_price * (1 - entry_multiplier)

        # Long or Short Entry, n minutes after RTH open
        if not HasTraded:
            # if data.at[idx - (window-1), 'Time'] == rth_start:
            if not np.isnan(long_entry) and not np.isnan(short_entry):
                close_price = row['close']
                if close_price > long_entry:
                    data.at[idx, 'Signal'] = 1  # Buy Signal
                    long_limit = open_price * (1 + limit_multiplier)
                    long_stop = open_price * (1 + stop_multiplier)
                    HasTraded = True
                    isLong = True
                elif close_price < short_entry:
                    data.at[idx, 'Signal'] = -1 
                    short_limit = open_price * (1 - limit_multiplier)
                    short_stop = open_price * (1 - stop_multiplier)
                    HasTraded = True
                    isShort = True

        # Exit End of Day
        if row['Time'] == rth_end:
            data.at[idx, 'Signal'] = 0  # Flatten position
            HasTraded = False
            isShort = False
            isLong = False

        # Manage open trade (Exit conditions)
        if isLong: 
            if row['high'] > long_limit or row['low'] < long_stop:  # Limit hit or stop hit
                data.at[idx, 'Signal'] = 0  # Flatten position
                isLong = False
        elif isShort: 
            if row['high'] > short_stop or row['low'] < short_limit:  # Limit hit or stop hit
                data.at[idx, 'Signal'] = 0  # Flatten position
                isShort = False

    # Fill 'Signal' with the last valid value (carry-forward)
    data['Signal'] = data['Signal'].ffill()

    return data
