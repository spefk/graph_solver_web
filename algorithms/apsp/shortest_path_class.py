from algorithms.graphs.graph_class import Graph
from algorithms.apsp.shortest_path_dijkstra import Dijkstra
from algorithms.apsp.shortest_path_floyd import FloydWarshall


class ShortestPathFinder:
    """
        Class that solves APSP, SP problems, using algorithms: Floyd-Warshal, Dijkstra.
        Class initializes with graph as networkx.Graph class, and flag
        negative_weight_flag which is 1 if there are edges with weight < 0 in graph.
    """

    def __init__(self, graph: Graph, negative_weights_flag: bool = False):
        self.graph = graph
        self.negative_weights_flag = negative_weights_flag

        self.dijkstra = Dijkstra()
        self.floyd = FloydWarshall()

        self.check_negativeness()

    # Updating of graph data causes drop of any computation results,
    # hence algorithm's realisation is not persistent in any way.
    def renew_graph(self, graph: Graph, negative_weights_flag: bool = False):
        self.__init__(graph, negative_weights_flag)

    # Protection: check if there are negative edges:
    def check_negativeness(self):
        if not self.negative_weights_flag:
            for edge in self.graph.edge_list:
                if edge.weight < 0:
                    self.negative_weights_flag = True
                    break

    # Returns sp distance between pair of vertices.
    def sp_pair_distances(self, start_node: int, end_node: int):
        if self.negative_weights_flag:
            return self.floyd.get_distance(self.graph, start_node, end_node)
        else:
            return self.dijkstra.get_distance(self.graph, start_node, end_node)

    # Gives sp between pair of vertices.
    def sp_pair_path(self, start_node: int, end_node: int):
        if self.negative_weights_flag:
            return self.floyd.get_path(self.graph, start_node, end_node)
        else:
            return self.dijkstra.get_path(self.graph, start_node, end_node)

    # Gives 1 to all distance vector
    def sp_one_to_all(self, s):
        if self.negative_weights_flag:
            self.dijkstra.run(self.graph, s)
            return self.dijkstra.distances
        else:
            self.floyd.run(self.graph)
            return self.floyd.distances[s]

    # Gives distance matrix
    def sp_all_to_all(self):
        self.floyd.run(self.graph)
        return self.floyd.distances
