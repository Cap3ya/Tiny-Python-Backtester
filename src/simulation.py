def simulate_trades(data):
    """
    Simulate trades and account for transaction costs.
    Args:
        data: DataFrame with 'Signal' column indicating trade signals.
    Returns:
        DataFrame with trading performance.
    """
    data['Position'] = data['Signal'].shift() # Enter after Signal Bar 
    data['Market_Return'] = data['close'].pct_change()
    data['Strategy_Return'] = data['Position'] * data['Market_Return']  # Gross returns
    
    data['Trade'] = data['Position'].diff().abs()  # Trade occurs when position changes
    
    data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()
    data['Cumulative_Market'] = (1 + data['Market_Return']).cumprod()
    data.to_csv('backtestingStrategy.csv')
    
    print(f"Return: {data['Cumulative_Strategy'].iloc[-1]:.2f}")
    return data

def calculate_performance(data):
    """
    Calculate key performance metrics for the strategy.
    """
    total_strategy_return = data['Cumulative_Strategy'].iloc[-1] - 1
    total_market_return = data['Cumulative_Market'].iloc[-1] - 1
    sharpe_ratio = data['Strategy_Return'].mean() / data['Strategy_Return'].std() * (252**0.5)
    max_drawdown = (data['Cumulative_Strategy'] / data['Cumulative_Strategy'].cummax() - 1).min()
    total_trades = data['Trade'].sum()

    return {
        'Total Strategy Return': f"{total_strategy_return:.2%}",
        'Total Market Return': f"{total_market_return:.2%}",
        'Sharpe Ratio': f"{sharpe_ratio:.2f}",
        'Max Drawdown': f"{max_drawdown:.2%}",
        'Total Trades': int(total_trades)
    }
