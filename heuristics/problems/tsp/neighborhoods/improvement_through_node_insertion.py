import random
from ..problem import TSP
from ....common import Neighborhood

class Node_insertion(Neighborhood):
    
    def __init__(self):
        super()

    def find_best(self, problem:TSP, solution:list[int], obj:float|None=None) -> tuple[list,float]:
        neighbor = solution.copy()
        neighbor_obj = obj if obj is not None else problem.evaluate(neighbor)

        best_i, best_j = None, None
        best_delta = 0
        for i in range(len(solution)):
            for j in range(len(solution)):
                if i != j:
                    node_to_insert = neighbor[i]
                    delta = (
                        problem.cost(neighbor[i - 1], node_to_insert)
                        + problem.cost(node_to_insert, neighbor[j])
                        - problem.cost(neighbor[i - 1], neighbor[i])
                        - problem.cost(neighbor[i], neighbor[j])
                    )

                    if delta < best_delta:
                        best_i, best_j, best_node = i, j, node_to_insert
                        best_delta = delta

        if best_i is not None and best_j is not None and best_node is not None:
            # Apply node insertion move
            neighbor.pop(best_i)
            neighbor.insert(best_j, best_node)
            neighbor_obj = neighbor_obj + best_delta

        return neighbor, neighbor_obj
    

    def find_better(self, problem:TSP, solution:list[int], obj:float|None=None) -> tuple[list,float]:
        neighbor = solution.copy()
        neighbor_obj = obj if obj is not None else problem.evaluate(neighbor)

        for i in range(len(solution)):
            for j in range(len(solution)):
                if i != j:
                    node_to_insert = neighbor[i]
                    delta = (
                        problem.cost(neighbor[i - 1], node_to_insert)
                        + problem.cost(node_to_insert, neighbor[j])
                        - problem.cost(neighbor[i - 1], neighbor[i])
                        - problem.cost(neighbor[i], neighbor[j])
                    )
   
                    if delta < -1e-6:
                        neighbor.pop(i)
                        neighbor.insert(j, node_to_insert)
                        neighbor_obj = neighbor_obj + delta

        return neighbor, neighbor_obj


    def find_any(self, problem:TSP, solution:list[int], obj:float|None=None, rng:random.Random=random) -> tuple[list[int],float]:
        neighbor = solution.copy()
        neighbor_obj = obj if obj is not None else problem.evaluate(neighbor)

        i = rng.randint(0, len(neighbor)-1)
        j = rng.randint(0, len(neighbor)-1)
        if i != j:
            node_to_insert = neighbor[i]
            delta = (
                problem.cost(neighbor[i - 1], node_to_insert)
                + problem.cost(node_to_insert, neighbor[j])
                - problem.cost(neighbor[i - 1], neighbor[i])
                - problem.cost(neighbor[i], neighbor[j])
            )
            neighbor.pop(i)
            neighbor.insert(j, node_to_insert)
            neighbor_obj = neighbor_obj + delta

        return neighbor, neighbor_obj