import random
from ..problem import TSP
from ....common import Neighborhood


class Triple_switch(Neighborhood):
    """3 switch neighborhood for the TSP.
    """

    def __init__(self):
        super()

    def find_best(self, problem:TSP, solution:list[int], obj:float|None=None) -> tuple[list,float]:
        neighbor = solution.copy()
        neighbor_obj = obj if obj is not None else problem.evaluate(neighbor)

        best_i, best_j, best_k = None, None, None
        best_delta = 0 
        for i in range(0, len(solution)):
            for j in range(i + 2, len(solution) - 1):
                for k in range(j + 2, len(solution) - 1):
                    delta = (
                        problem.cost(solution[i - 1], solution[j])
                        + problem.cost(solution[j], solution[(i + 1) % len(solution)])
                        + problem.cost(solution[j - 1], solution[k])
                        + problem.cost(solution[k], solution[(j + 1) % len(solution)])
                        + problem.cost(solution[k - 1], solution[i])
                        + problem.cost(solution[i], solution[(k + 1) % len(solution)])
                        - problem.cost(solution[i - 1], solution[i])
                        - problem.cost(solution[i], solution[(i + 1) % len(solution)])
                        - problem.cost(solution[j - 1], solution[j])
                        - problem.cost(solution[j], solution[(j + 1) % len(solution)])
                        - problem.cost(solution[k - 1], solution[k])
                        - problem.cost(solution[k], solution[(k + 1) % len(solution)])
                    )
                    if delta < best_delta:
                        best_i, best_j, best_k = i, j, k
                        best_delta = delta

        if best_i is not None and best_j is not None and best_k is not None:
            neighbor[best_i], neighbor[best_j], neighbor[best_k] = neighbor[best_j], neighbor[best_k], neighbor[best_i]
            neighbor_obj = neighbor_obj + best_delta
        
        return neighbor, neighbor_obj
    

    def find_better(self, problem:TSP, solution:list[int], obj:float|None=None) -> tuple[list,float]:
        neighbor = solution.copy()
        neighbor_obj = obj if obj is not None else problem.evaluate(neighbor)

        for i in range(0, len(solution)):
            for j in range(i + 2, len(solution) - 1):
                for k in range(j + 2, len(solution) - 1):    
                    delta = (
                        problem.cost(solution[i - 1], solution[j])
                        + problem.cost(solution[j], solution[(i + 1) % len(solution)])
                        + problem.cost(solution[j - 1], solution[k])
                        + problem.cost(solution[k], solution[(j + 1) % len(solution)])
                        + problem.cost(solution[k - 1], solution[i])
                        + problem.cost(solution[i], solution[(k + 1) % len(solution)])
                        - problem.cost(solution[i - 1], solution[i])
                        - problem.cost(solution[i], solution[(i + 1) % len(solution)])
                        - problem.cost(solution[j - 1], solution[j])
                        - problem.cost(solution[j], solution[(j + 1) % len(solution)])
                        - problem.cost(solution[k - 1], solution[k])
                        - problem.cost(solution[k], solution[(k + 1) % len(solution)])
                    )   
                    if delta < -1e-6:
                        neighbor[i], neighbor[j], neighbor[k] = neighbor[j], neighbor[k], neighbor[i]
                        neighbor_obj = neighbor_obj + delta
                        return neighbor, neighbor_obj
        
        return neighbor, neighbor_obj
    
    def find_any(self, problem:TSP, solution:list[int], obj:float|None=None, rng:random.Random=random) -> tuple[list[int],float]:
        neighbor = solution.copy()
        neighbor_obj = obj if obj is not None else problem.evaluate(neighbor)
        i, j, k = rng.sample(range(len(neighbor) - 2), 3)  # Seleciona 3 índices distintos aleatórios.
        delta = (
            problem.cost(neighbor[i - 1], neighbor[j])
            + problem.cost(neighbor[j], neighbor[(i + 1) % len(neighbor)])
            + problem.cost(neighbor[j - 1], neighbor[k])
            + problem.cost(neighbor[k], neighbor[(j + 1) % len(neighbor)])
            + problem.cost(neighbor[k - 1], neighbor[i])
            + problem.cost(neighbor[i], neighbor[(k + 1) % len(neighbor)])
            - problem.cost(neighbor[i - 1], neighbor[i])
            - problem.cost(neighbor[i], neighbor[(i + 1) % len(neighbor)])
            - problem.cost(neighbor[j - 1], neighbor[j])
            - problem.cost(neighbor[j], neighbor[(j + 1) % len(neighbor)])
            - problem.cost(neighbor[k - 1], neighbor[k])
            - problem.cost(neighbor[k], neighbor[(k + 1) % len(neighbor)])
        )
        neighbor[i], neighbor[j], neighbor[k] = neighbor[j], neighbor[k], neighbor[i]
        neighbor_obj = neighbor_obj + delta
        return neighbor, neighbor_obj