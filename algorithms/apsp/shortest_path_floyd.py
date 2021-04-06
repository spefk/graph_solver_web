from algorithms.graphs.graph_class import Graph
from copy import deepcopy


class FloydWarshall:
    """
        Class, that process graph and find APSP in it, using Floyd-Warshall algorithm.
        After first run it carries distance matrix and all successors, so all APSP could
        be found without redundant computations.
    """
    def __init__(self):
        self.distances = None
        self.successors = None

    def clear(self):
        self.__init__()

    # Main procedure of algorithm.
    def floyd_body(self, graph: Graph):
        # Algorithm goes by considering new vertex k as intermediate
        # in path u -> v for any u, v.
        for k in range(graph.vertex_number):
            for u in range(graph.vertex_number):
                for v in range(graph.vertex_number):
                    if self.distances[u][v] > self.distances[u][k] + self.distances[k][v]:
                        self.distances[u][v] = self.distances[u][k] + self.distances[k][v]
                        self.successors[u][v] = self.successors[u][k]

    # Find -inf sp
    def floyd_not_existing_sp(self, graph):
        dist_matrix = deepcopy(self.distances)
        self.floyd_body(graph)
        for u in range(graph.vertex_number):
            for v in range(graph.vertex_number):
                if dist_matrix[u][v] != self.distances[u][v]:
                    self.distances[u][v] = -float('inf')

    # Floyd-Warshall algorithm.
    def floyd(self, graph: Graph):
        self.distances = [[min([edge.weight for edge in graph.get_edges(v1, v2)], default=float('inf'))
                           for v2 in range(graph.vertex_number)] for v1 in range(graph.vertex_number)]
        self.successors = [[float('inf')] * graph.vertex_number for _ in graph.vertex_list]

        # Initialize algorithm distance matrix and predecessors.
        for u in range(graph.vertex_number):
            self.distances[u][u] = 0
            for v in range(graph.vertex_number):
                if self.distances[u][v] != float('inf'):
                    self.successors[u][v] = v

        self.floyd_body(graph)
        # Second run to collect all negative cycles
        self.floyd_not_existing_sp(graph)

    # The oracle, that runs FW algorithm, if it is necessary.
    def run(self, graph: Graph):
        if self.distances is None:
            self.floyd(graph)

    # Gives sp distance between pair of vertices.
    def get_distance(self, graph: Graph, start_node: int, end_node: int):
        self.run(graph)
        return self.distances[start_node][end_node]

    # Gives sp between pair of vertices.
    def get_path(self, graph: Graph, start_node: int, end_node: int):
        self.run(graph)

        if abs(self.distances[start_node][end_node]) == float('inf'):
            return []
        cur_vert = start_node
        path = [cur_vert]
        while True:
            cur_vert = self.successors[cur_vert][end_node]
            path.append(cur_vert)
            if cur_vert is end_node:
                break
        return path

    # Prints distance matrix and successors matrix.
    def print_matrix(self):
        try:
            print('distance matrix:', *self.distances, sep='\n')
            print('successors matrix:', *self.successors, sep='\n')
        except Exception as exc:
            print(f'Floyd is cold. {repr(exc)}')
            raise exc
