from algorithms.graphs.graph_class import *
from algorithms.graphs.graph_walk_functions import *


class GraphWalk:
    def __init__(self):
        self.visited = []
        self.graph = Graph()

    def reset(self):
        self.graph = Graph
        self.visited = []


class DFS(GraphWalk):
    def __init__(self):
        super().__init__()

    def dfs_recursive(self, vertex, in_function=pass_function, out_function=pass_function):
        for v in self.graph.vertex_adjacency[vertex]:
            if self.visited[v.name] == 0:
                self.visited[v.name] = 1
                in_function(v.name, predc=vertex)
                self.dfs_recursive(v.name, in_function=in_function, out_function=out_function)
                out_function(v.name, predc=vertex)

    def dfs(self, graph: Graph, start_vertex, in_function=pass_function, out_function=pass_function):
        self.graph = graph
        self.visited = [0] * graph.vertex_number
        in_function(start_vertex, predc='initialization.')
        self.visited[start_vertex] = 1
        self.dfs_recursive(start_vertex, in_function=in_function, out_function=out_function)
        out_function(start_vertex, predc='execution is over.')
        visited = self.visited.copy()
        self.reset()
        return visited


class BFS(GraphWalk):
    def __init__(self):
        super().__init__()
        self.queue = []

    def bfs_procedural(self, in_function=pass_function):
        while self.queue:
            cur_vert = self.queue.pop()
            if self.visited[cur_vert] == 0:
                self.visited[cur_vert] = 1
                in_function(cur_vert)
                for v in self.graph.vertex_adjacency[cur_vert]:
                    self.queue.insert(0, v.name)

    def bfs(self, graph: Graph, start_vertex, in_function=pass_function):
        self.graph = graph
        self.visited = [0] * graph.vertex_number
        self.queue = [start_vertex]
        self.bfs_procedural(in_function=in_function)
        visited = self.visited.copy()
        self.reset()
        return visited
