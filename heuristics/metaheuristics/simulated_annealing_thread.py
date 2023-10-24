import math
import random
from collections.abc import Callable
from ..common import Problem
from ..common import Neighborhood
from ..common import CustomThread

def simulated_annealing_child(
    k_max,
    problem,
    solution,
    obj,
    neighborhood_function,
    rng,
    temperature,
    cooling_rate,
    initial_temp,
    best_solution,
    best_obj
    ) -> tuple[object,int|float]:
    
    for k in range(1, k_max + 1):
        neighbor, neighbor_obj = neighborhood_function.find_any(problem, solution, obj, rng)
        delta = neighbor_obj - obj
        if delta <= 0:
            solution, obj = neighbor, neighbor_obj
            if neighbor_obj < best_obj:
                best_solution, best_obj = neighbor, neighbor_obj
            else:
                r = rng.random()
                if r < math.exp(- delta/ temperature):
                    solution, obj = neighbor, neighbor_obj
        
    return best_solution, best_obj

def simulated_annealing_main(
    problem : Problem,
    start_solution : object,
    start_obj: int|float,
    neighborhood_function : Neighborhood,
    initial_temp : int|float,
    cooling_rate : int|float,
    k_max : int|float,
    n_threads: int,
    max_iter: float=math.inf,
    rng: random.Random=random,
    eps: float=1e-6,
    cb: Callable[[int,object,int|float],None]=lambda iter, solution, obj: None
) -> tuple[object,int|float]:
    """Simulated Annealing algorithm


    :param problem: The problem to solve
    :param start_solution: The initial solution.
    :param start_obj: The value of objective function for the initial solution (optional).
    :param neighborhood_function: The neighborhood function.
    :param initial_temp: The initial value of temperature.
    :param cooling_rate: The cooling rate.
    :param k_max: Max number of iterations for each value of temperature.
    :param max_iter: The maximum number of iterations.
    :param n_thread: The number of threads.
    :param rng: The random number generator (optional, default is to use the random module).
    :param eps: The precision used for comparing objective function values (default is 1e-6).
    :param cb: A callback function that is called after each iteration (optional). 
    :return: A tuple containing the best solution found and its objective function value.
    """
    best_solution, best_obj = start_solution, start_obj   
    solution, obj = start_solution, start_obj
    temperature = initial_temp
    iter = 0
    cb(iter, best_solution, best_obj)
    while iter != max_iter :
        thread_list = [
            CustomThread(
                target=simulated_annealing_child,
                args=(
                    k_max,
                    problem,
                    solution,
                    obj,
                    neighborhood_function,
                    rng,
                    temperature,
                    cooling_rate,
                    initial_temp,
                    best_solution,
                    best_obj
                )) for n in range(1, n_threads +1)
        ]

        # compara os resultados obtidos nas threads
        
        for thread in thread_list:
            thread.start()
            if thread.join()[1] < best_obj:
                best_solution = thread.join()[0]
                best_obj = thread.join()[1]
    
        temperature = cooling_rate * temperature
        if temperature < eps:
            temperature = initial_temp
        iter += 1
        cb(iter, best_solution, best_obj)
    return best_solution, best_obj
    

