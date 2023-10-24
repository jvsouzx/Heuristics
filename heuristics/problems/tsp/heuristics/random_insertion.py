import math
import random
from ..problem import TSP

def random_insertion_heuristic(problem: TSP, start_node: int, rng: random.Random=random) -> tuple[list[int], float]:
    """Generates a solution for the TSP problem using the random insertion heuristic.

    The random insertion heuristic starts at one node and then, repeatedly finds the 
    node not already in the tour randomly. It then inserts the node into the position 
    that minimizes the increase in the total cost. It stops when all nodes have been visited.

    The time complexity of the farthest insertion algorithm is O(n^2).
    
    :param problem: The TSP problem.
    :param start_node: The node to start the solution from.
    :param rng: The random number generator (optional, default is to use the random module).
    :return: A solution obtained with the nearest insertion heuristic and its cost.
    """
    solution = [start_node]
    nodes = problem.nodes()
    nodes.remove(start_node)
    while len(nodes) > 0:

        # select a random node
        random_node = rng.choice(nodes)
        best_cost = 0
        # Insert node into a position that minimizes the increase in the cost
        best_index = len(solution)
        best_cost = math.inf
        if (len(solution) > 1):
            for i in range(0, len(solution) ):
                cost = (problem.cost(solution[i-1], random_node)  
                        + problem.cost(random_node, solution[i]) 
                        - problem.cost(solution[i-1], solution[i]))
                if cost < best_cost:
                    best_index = i
                    best_cost = cost
            
        # Update the solution and the list of nodes
        solution.insert(best_index, random_node)
        nodes.remove(random_node)
            
    return solution, problem.evaluate(solution)