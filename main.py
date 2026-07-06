import numpy as np
from mealpy import GA
from mealpy import FloatVar
from joblib import Parallel, delayed
from opfunu import get_functions_by_classname

# Genetic Algorithm settings
SearchAgents = 30          # Population size
Max_iter = 1000            # Number of iterations
num_runs = 30              # Number of independent runs for each benchmark

# Dictionary to store statistics for all benchmarks
statistics_all_benchmarks = dict()

def GAF(SearchAgents, Max_iter, test_function, lb, ub, dim):
    """
    Genetic Algorithm (GA) optimization function.
    Args:
        SearchAgents (int): Number of agents (population size).
        Max_iter (int): Number of iterations.
        test_function (function): Objective function to minimize.
        lb (float): Lower bound of variables.
        ub (float): Upper bound of variables.
        dim (int): Dimension of the problem.

    Returns:
        tuple: Best solution, best fitness score, convergence curve.
    """
    problem = {
        "obj_func": test_function,
        "bounds": FloatVar(lb=(float(lb), )*dim, ub=(float(ub), )*dim),
        "minmax": "min",
        "log_to": None,
    }

    model = GA.BaseGA(Max_iter, SearchAgents, pc=0.999999, pm=0.1)
    g_best = model.solve(problem)

    return g_best.solution, g_best.target.fitness, model.history.list_global_best_fit

# Main optimization loop
for algo_D in ['GA_10D', 'GA_20D']:
    statistics_all_benchmarks[algo_D] = []
    print(f"Running {algo_D}")

    for fn in range(1, 13):
        # Get the test function from opfunu
        cec2022 = get_functions_by_classname(f"F{fn}2022")
        dim = int(algo_D[-3:-1])
        cec = cec2022[0](dim)

        # Lists to store results of multiple runs
        best_pos_list = []
        best_score_list = []
        curve_list = []

        # Run multiple instances of the GA in parallel
        results = Parallel(n_jobs=-1)(delayed(GAF)(
            SearchAgents, Max_iter, cec.evaluate, cec.lb[0], cec.ub[0], dim) for _ in range(num_runs))

        # Collect results
        for best_pos, best_score, convergence_curve in results:
            best_pos_list.append(best_pos)
            best_score_list.append(best_score)
            curve_list.append(convergence_curve)

        # Find the best result among all runs
        best_idx = np.argmin(best_score_list)

        # Store statistics
        statistics_all_benchmarks[algo_D].append({
            'Fn': f'F{fn}',
            "Mean": f'{np.mean(best_score_list):.3E}',
            "Best": f'{np.min(best_score_list):.3E}',
            "Worst": f'{np.max(best_score_list):.3E}',
            "Median": f'{np.median(best_score_list):.3E}',
            "STD": f'{np.std(best_score_list):.3E}',
            'Best_position': best_pos_list[best_idx],
            'Curve': curve_list[best_idx],
            'Best_result': best_score_list,
        })

        # Print summarized results
        print(dict(list(statistics_all_benchmarks[algo_D][-1].items())[:6]))
