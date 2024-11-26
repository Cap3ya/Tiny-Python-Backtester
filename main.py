from strategies.change_from_open_strategy_v2 import change_from_open_strategy_v2
from optimizer import optimize_strategy
from data_loader import load_data
from simulation import simulate_trades
from plotter import plot_results

if __name__ == "__main__":
    file_path = "NQ_1min-2022-11-22_2024-11-22.csv"
    # file_path = "NQ_1min-2023-11-22_2024-11-22.csv"

    # Strategy selection
    strategy_func = change_from_open_strategy_v2
    param_grid = {
        'window': [1, 5, 15, 30, 60],
        'threshold': [0.05, 0.1, 0.5, 1],

        # 'stop_multiplier': [-0.4, -0.2, -0],
        # 'limit_multiplier': [1, 2],
        # 'entry_multiplier': [0.4, 0.2]
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
