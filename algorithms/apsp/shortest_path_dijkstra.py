from algorithms.graphs.graph_class import Graph, UndirectedGraph, DirectedGraph
import heapq


class Dijkstra:
    """
        Class, that process graph and find SP from u to any other vertex in
        graph with POSITIVE WEIGHTS. It carries all distances and path info
        after run on u, and refreshes it if next call vertex v != u.
    """
    def __init__(self):
        self.start_node = None
        self.distances = None
        self.predecessors = None

    def clear(self):
        self.__init__()

    # Dijkstra's algorithm. Using min heap.
    def dijkstra(self, graph: Graph, start_node: int):

        self.start_node = start_node

        self.distances = [float('inf')] * graph.vertex_number
        self.predecessors = [float('inf')] * graph.vertex_number
        used = [False] * graph.vertex_number

        min_heap = []

        heapq.heappush(min_heap, (0, start_node))
        self.predecessors[start_node] = -1
        self.distances[start_node] = 0
        for _ in range(graph.vertex_number):
            while True:
                try:
                    v = heapq.heappop(min_heap)[1]
                    if not used[v]:
                        v_distances = self.distances[v]
                        used[v] = True
                        break
                except IndexError:
                    v = float('inf')
                    v_distances = float('inf')
                    break

            if v_distances == float('inf'):
                break

            for vert in graph.vertex_adjacency[v]:
                u = vert.name
                for edge in graph.get_edges(v, u):
                    w = edge.weight
                    if self.distances[u] > v_distances + w:
                        self.distances[u] = v_distances + w
                        self.predecessors[u] = v
                        heapq.heappush(min_heap, (self.distances[u], u))

    # Oracle, that runs Dijkstra's algorithm when it is necessary.
    def run(self, graph: Graph, start_node: int):
        if self.start_node is not start_node:
            self.dijkstra(graph, start_node)

    # Gives sp distance between pair of vertices.
    def get_distance(self, graph: Graph, start_node: int, end_node: int):
        self.run(graph, start_node)
        return self.distances[end_node]

    # Gives sp between pair of vertices.
    def get_path(self, graph: Graph, start_node: int, end_node: int):
        self.run(graph, start_node)
        path = []
        cur_node = end_node
        while True:
            path.insert(0, cur_node)
            if cur_node is start_node:
                break
            cur_node = self.predecessors[cur_node]
            if cur_node == float('inf'):
                return []
        return path
