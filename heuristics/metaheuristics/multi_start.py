import math
import time
import random
from collections.abc import Callable
from ..common import Problem


def multistart(
    problem: Problem,
    local_search: Callable[[Problem,object,int|float,random.Random], tuple[object,int|float]],
    create_random_solution: Callable[[Problem,object,int|float,random.Random], tuple[object,int|float]],
    rng: random.Random=random,
    eps: float=1e-6,
    cb: Callable[[int,object,int|float],None]=lambda iter, solution, obj: None
) -> tuple[object,int|float]:
    """Multi Start algorithm.

    :param problem: The problem to solve.
    :param local_search: The local method.
    :param perturbation: The perturbation method.
    :param start_solution: The initial solution.
    :param start_obj: The value of objective function for the initial solution (optional).
    :param rng: The random number generator (optional, default is to use the random module).
    :param eps: The precision used for comparing objective function values (default is 1e-6).
    :param max_iter: The maximum number of iterations (default is 100).
    :param max_iter_no_improv: The maximum number of iterations without improvement (default is 25).
    :param max_time: Time limit in seconds (optional, default is math.inf).
    :param cb: A callback function that is called after each iteration (optional).
    :return: A tuple containing the best solution found and its objective function value.
    """
    best_solution = None
    best_obj = math.inf

    iter = 1

    while (True):
        solution, obj = create_random_solution(problem, rng)
        solution, obj = local_search(problem, solution, obj, rng)
        if obj < best_obj:
            best_solution = solution
            best_obj = obj
            cb(iter, best_solution, best_obj)
        iter+=1
    return best_solution, best_obj
