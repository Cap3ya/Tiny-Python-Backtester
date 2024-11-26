import pandas as pd
import databento as db

def fetch_data():
    # Initialize the DataBento client
    client = db.Historical('db-KXXLa8Pif7NypiMNcBg7tUP5N8ya8')

    # Retrieve historical data for a 2-year range
    data = client.timeseries.get_range(
        dataset='GLBX.MDP3',       # CME dataset
        schema='ohlcv-1m',         # 1-min aggregates
        stype_in='continuous',     # Symbology by lead month
        symbols=['NQ.v.0'],        # Front month by Volume
        start='2022-11-22',
        end='2024-11-22',
    )

    # Save to CSV
    data.to_csv('NQ_1min-2022-11-22_2024-11-22.csv')

def load_data(file_path):
    """
    Reads a CSV file, selects relevant columns, converts 'ts_event' to datetime,
    and converts the time from UTC to Eastern Time.
    
    Parameters:
    - file_path: str, path to the CSV file.
    
    Returns:
    - df: pandas DataFrame with processed data.
    """
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Keep only relevant columns (ts_event, open, high, low, close, volume)
    df = df[['ts_event', 'open', 'high', 'low', 'close', 'volume']]

    # Convert the 'ts_event' column to pandas datetime format (UTC)
    df['ts_event'] = pd.to_datetime(df['ts_event'], utc=True)

    # Convert UTC to Eastern Time (US/Eastern)
    df['ts_event'] = df['ts_event'].dt.tz_convert('US/Eastern')

    # Filter for RTH (9:30 AM to 4:00 PM ET) directly on the 'ts_event' column
    df = df[df['ts_event'].dt.time.between(pd.to_datetime("09:30", format="%H:%M").time(), pd.to_datetime("16:00", format="%H:%M").time())]
    # Reset the index
    df.reset_index(inplace=True, drop=True)
    
    # Add Date and Time columns
    df['Date'] = df['ts_event'].dt.date
    df['Time'] = df['ts_event'].dt.time
    
    return df
