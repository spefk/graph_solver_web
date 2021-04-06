from algorithms.graphs.graph_class import UndirectedGraph, DirectedGraph
from algorithms.graphs.graph_walk_classes import DFS, BFS, print_on_enter, print_on_exit
from algorithms.graphs.graph_visualization import GraphVisualizer

"""
    Testing samples and testing algorithms run.
"""

if __name__ == '__main__':
    dfs = DFS()
    bfs = BFS()

    # Undirected Graphs

    graph = UndirectedGraph()

    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(6, 5)
    graph.add_edge(3, 7)

    print(dfs.dfs(graph, 1, in_function=print_on_enter, out_function=print_on_exit))

    print(graph.vertex_map)

    # Directed Graphs

    dir_graph = DirectedGraph()

    dir_graph.add_edge(1, 2)
    dir_graph.add_edge(4, 5)
    dir_graph.add_edge(6, 5)
    dir_graph.add_edge(7, 6)
    dir_graph.add_edge(2, 3)
    dir_graph.add_edge(2, 4)

    print(dfs.dfs(dir_graph, 0, in_function=print_on_enter, out_function=print_on_exit))

    print(dir_graph.vertex_map)

    print(bfs.bfs(dir_graph, 0, in_function=print_on_enter))

    # visualization
    graph_vis = GraphVisualizer(graph, directedQ=True)
    graph_vis.visualize_graph(highlight_edges=[(2, 6), (0, 2)])

    # mutable objects test
    graph = UndirectedGraph()
    graph.add_edge(1, 2, weight=-10)

    for edge in graph.edge_list:
        print(f"{edge}, {edge.weight}")

    graph.edge_dict[(0, 1)][0].weight = 0

    for edge in graph.edge_list:
        print(f"{edge}, {edge.weight}")
