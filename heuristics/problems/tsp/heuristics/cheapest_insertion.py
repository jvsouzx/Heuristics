import math
from ..problem import TSP

def cheapest_insertion_heuristic(problem: TSP, start_node: int) -> tuple[list[int], float]:
    """Generates a solution for the TSP problem using the cheapest insertion heuristic.

    The cheapest insertion heuristic starts with a single node and repeatedly selects the node
    that, when inserted into the tour, results in the smallest increase in total cost. It stops when
    all nodes have been visited.

    The time complexity of the cheapest insertion algorithm is O(n^3).

    :param problem: The TSP problem.
    :param start_node: The node to start the solution from.
    :return: A solution obtained with the Cheapest Insertion heuristic and its cost.
    """


    # The next node to join the tour, T, is the one that minimizes c(i, k, j) among all the 
    # nodes k E (N-T) and for all consecutive pairs of nodes (i, j) E T. The location where 
    # the selected node is inserted is, of course, the one that minimizes c(i, k, j). The 
    # procedure is repeated until all nodes have been inserted into T.
    
    solution = [start_node]
    nodes = problem.nodes()
    nodes.remove(start_node)
    
    while len(nodes) > 0:
        best_node = None
        best_cost = math.inf
        best_index = None
        
        for node in nodes:
            for i in range(len(solution)):
                # Calculate the cost increase if we insert 'node' between positions i and j
                cost = (
                    problem.cost(solution[i], node) + problem.cost(node, solution[(i + 1) % len(solution)])
                    - problem.cost(solution[i], solution[(i + 1) % len(solution)])
                )
                
                if cost < best_cost:
                    best_node = node
                    best_cost = cost
                    best_index = i
        
        # Update the solution and the list of nodes
        solution.insert(best_index, best_node)
        nodes.remove(best_node)
    
    return solution, problem.evaluate(solution)