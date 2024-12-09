import matplotlib.pyplot as plt

def plot_results(data):
    """
    Plot cumulative returns for the strategy and the market.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Cumulative_Strategy'], label='Strategy', linewidth=2)
    plt.plot(data.index, data['Cumulative_Market'], label='Market (Buy & Hold)', linewidth=2)
    plt.legend()
    plt.title('Backtest Results')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.grid()
    plt.show()
