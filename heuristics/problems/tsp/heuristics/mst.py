from ..problem import TSP
import networkx as nx

def minimum_spanning_tree(problem: TSP, start_node: int) -> tuple[list[int], float]:
    
    graph = nx.Graph()
    for u, v in problem.get_edges():
        weight = problem.cost(u, v)
        graph.add_edge(u, v, weight=weight)
    
    graph.remove_node(start_node)
    mst = nx.minimum_spanning_tree(graph)
    eulerian_graph = nx.MultiGraph()
    
    for u, v in mst.edges():
        weight = mst[u][v]['weight']
        eulerian_graph.add_edge(u, v, weight=weight)
        eulerian_graph.add_edge(v, u, weight=weight)
    
    eulerian_tour = list(nx.eulerian_circuit(eulerian_graph))
    visited = set()
    solution = []
    
    for node in eulerian_tour:
        if node not in visited:
            solution.append(node[0])
            visited.add(node)

    return solution, problem.evaluate(solution)