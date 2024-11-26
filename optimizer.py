from itertools import product
from data_loader import load_data
from simulation import simulate_trades, calculate_performance

def optimize_strategy(file_path, strategy_func, param_grid, performance_metric='Total Strategy Return'):
    """
    Optimize strategy parameters using a grid search approach.
    """
    param_combinations = list(product(*param_grid.values()))
    param_names = list(param_grid.keys())
    
    best_params = None
    best_performance = None
    best_metric_value = -float('inf')

    for param_values in param_combinations:
        params = dict(zip(param_names, param_values))
        
        data = load_data(file_path)
        data = strategy_func(data, **params)
        data = simulate_trades(data)
        performance = calculate_performance(data)
        
        metric_value = float(performance[performance_metric].strip('%'))
        if performance_metric == 'Sharpe Ratio':
            metric_value = float(performance[performance_metric])
        
        if metric_value > best_metric_value:
            best_metric_value = metric_value
            best_params = params
            best_performance = performance

    return best_params, best_performance
