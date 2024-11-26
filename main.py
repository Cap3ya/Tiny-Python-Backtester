from strategies.opening_range_strategy import opening_range_strategy
from optimizer import optimize_strategy
from data_loader import load_data
from simulation import simulate_trades
from plotter import plot_results

if __name__ == "__main__":
    file_path = "NQ_1min-2022-11-22_2024-11-22.csv"
    # file_path = "NQ_1min-2023-11-22_2024-11-22.csv"

    # Strategy selection
    strategy_func = opening_range_strategy
    param_grid = {
        'window': [1, 5, 15, 30, 60],
    }
    
    # Optimize strategy
    best_params, best_performance = optimize_strategy(
        file_path,
        strategy_func,
        param_grid,
    )
    print("Best Parameters:", best_params)
    print("Performance Metrics:", best_performance)
    
    # Backtest with best parameters
    data = load_data(file_path)
    data = strategy_func(data, **best_params)
    data = simulate_trades(data)
    plot_results(data)
