import sys
import math
import random
from threading import Thread

import heuristics.problems.tsp as tsp
import heuristics.local_search as ls
import heuristics.metaheuristics as mh

# -------------------------------------------------------------------
# -------------------------------------------------------------------

# Your code here!
def solver(problem, rng, cb):

    ns = [tsp.Shift()]

    def local_search(problem, solution, obj, rng):
        return ls.vnd(problem, ns, solution, obj, False)
    
    def create_rand_solution(problem, rng):
        return tsp.random_heuristic(problem, rng)
    
    def perturbation(problem, solution, obj, rng):
        for _ in range(rng.randint(5, 10)):
            solution, obj = ns[0].find_any(problem, solution, obj, rng)
        return solution, obj

    solution, obj = tsp.furthest_insertion_heuristic(problem, 15)
    #solution, obj = mh.ils(problem, local_search, perturbation, solution, obj, rng=rng, cb=cb)
    #solution, obj = mh.multistart(problem, local_search, create_rand_solution, rng=rng, cb=cb)
    solution, obj  = mh.simulated_annealing_main(problem, solution, obj, ns[0], 10000, 0.95, 100, 3, 1000, rng, cb=cb)

    
# -------------------------------------------------------------------
# -------------------------------------------------------------------

# Some globals
global problem, best_solution, best_obj
problem = None
best_obj = None
best_obj = math.inf

# Callback function
def cb(iter, solution, obj):
    global problem, best_solution, best_obj
    obj = problem.evaluate(solution)
    if obj + 1e-6 < best_obj:
        best_solution = solution
        best_obj = obj
        print(f'Iteration {iter}: {best_obj}')

# CLI arguments
instance = sys.argv[1]
seed = int(sys.argv[2])
timelimit = float(sys.argv[3])

# Initialize random number generator
rng = random.Random(seed)

# Load problem
problem = tsp.TSP(instance)

# Solve problem
process = Thread(target=solver, args=(problem, rng, cb))
process.daemon=True
process.start()
process.join(timeout=timelimit)
