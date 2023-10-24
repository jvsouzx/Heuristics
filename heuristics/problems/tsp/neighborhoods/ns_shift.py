import random
from ..problem import TSP
from ....common import Neighborhood


class Shift(Neighborhood):
    """Shift neighborhood for the TSP.
    """

    def __init__(self):
        super()

    def find_best(self, problem:TSP, solution:list[int], obj:float|None=None) -> tuple[list,float]:
        best_solution = solution.copy()
        best_obj = obj if obj is not None else problem.evaluate(best_solution)
        for i in range(0, len(solution)):
            node = solution[i]
            neighbor = solution.copy()
            neighbor.remove(node)
            for j in range(0, len(neighbor)):
                neighbor.insert(j, node)
                obj = problem.evaluate(neighbor)
                if obj < best_obj:
                    best_solution = neighbor.copy()
                    best_obj = obj

                neighbor.remove(node)

        return best_solution, best_obj

    def find_better(self, problem:TSP, solution:list[int], obj:float|None=None) -> tuple[list,float]:
        best_solution = solution.copy()
        best_obj = obj if obj is not None else problem.evaluate(best_solution)
        for i in range(0, len(solution)):
            node = solution[i]
            neighbor = solution.copy()
            neighbor.remove(node)
            for j in range(0, len(neighbor)):
                neighbor.insert(j, node)
                obj = problem.evaluate(neighbor)
                if obj < best_obj:
                    return neighbor, obj
                neighbor.remove(node)
                
        return best_solution, best_obj


    def find_any(self, problem:TSP, solution:list[int], obj:float|None=None, rng:random.Random=random) -> tuple[list[int],float]:
        neighbor = solution.copy()
        i = rng.randint(0, len(solution)-1)
        node = neighbor[i]
        neighbor = solution.copy()
        neighbor.remove(node)
        j = rng.randint(0, len(solution)-1)
        neighbor.insert(j, node)
        obj = problem.evaluate(neighbor)

        return neighbor, obj