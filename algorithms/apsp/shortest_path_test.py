from algorithms.apsp.shortest_path_class import ShortestPathFinder
from algorithms.graphs.graph_class import DirectedGraph
from algorithms.graphs.graph_visualization import GraphVisualizer

"""
    Testing samples and testing algorithms run.
"""

if __name__ == '__main__':

    # Test Undirected of Directed Graph Instance
    G = DirectedGraph()
    G.add_edge(0, 1, weight=1)
    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 3, weight=1)
    G.add_edge(1, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(2, 5, weight=10)

    G.add_edge(6, 7, weight=1)
    G.add_edge(7, 6, weight=-2)

    for u, lst in G.vertex_adjacency.items():
        print(f'{u}: {lst}')

    # Test ShortestPathFinder
    sp_finder = ShortestPathFinder(G)
    print(sp_finder.sp_pair_path(2, 5))
    print(sp_finder.sp_pair_distances(2, 5))
    print(sp_finder.sp_pair_path(2, 6))
    print(sp_finder.sp_pair_distances(2, 6))
    print(sp_finder.sp_pair_distances(6, 7))
    print(sp_finder.sp_pair_path(6, 7))

    sp_finder.floyd.print_matrix()
    print(sp_finder.sp_pair_path(0, 5))

    # sp_finder.dijkstra.run(sp_finder.graph, 1)
    # print(sp_finder.dijkstra.distances)
    gr_vis = GraphVisualizer(G)
    gr_vis.visualize_graph()
    tmp_path = sp_finder.sp_pair_path(0, 5)
    highlight = [(tmp_path[i], tmp_path[i + 1]) for i in range(len(tmp_path) - 1)]
    gr_vis.visualize_graph(highlight_edges=highlight)
