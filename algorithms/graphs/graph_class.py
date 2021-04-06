import networkx
from collections import defaultdict
from algorithms.graphs.graph_objects_classes import *
from abc import ABC, abstractmethod


class Graph(ABC):
    """
    Carries vertex and edge instances, and info about their interconnections.
    Being inherited by UndirectedGraph, DirectedGraph, Network classes.
    """
    def __init__(self, vertex_list=None, edge_list=None):
        if edge_list is None:
            edge_list = []
        if vertex_list is None:
            vertex_list = []

        self.vertex_list = []
        self.vertex_number = 0
        self.edge_number = 0
        self.edge_type = Edge
        self.vertex_map = dict()
        self.vertex_map_revert = dict()
        self.edge_list = []
        self.edge_dict = defaultdict(list)
        self.vertex_adjacency = defaultdict(list)

        self.add_vertex_list(vertex_list)
        self.add_edge_list(edge_list)

    def set_graph_networkx(self, graph: networkx.Graph):
        edges = list(graph.edges())
        self.__init__(edge_list=edges)

    def add_vertex_list(self, vertex_list: list):
        for vert in vertex_list:
            self.add_vertex(vert)

    def add_edge_list(self, edge_list: list):
        for edge in edge_list:
            self.add_edge(*edge)

    def add_vertex(self, vertex_name):
        """Adds vertex with name vertex_name. Enumerates vertices locally, using self.vertex_map."""
        if vertex_name not in self.vertex_map:
            self.vertex_map[vertex_name] = self.vertex_number
            self.vertex_map_revert[self.vertex_number] = vertex_name
            self.vertex_number += 1
            self.vertex_list.append(Vertex(self.vertex_map[vertex_name], tag=vertex_name))

    def edge_iterator(self):
        for lst in self.edge_dict.values():
            for edge in lst:
                yield edge

    def add_edge(self, prc=None, suc=None, weight=0):
        self.add_vertex(prc)
        self.add_vertex(suc)
        prc = self.vertex_map[prc]
        suc = self.vertex_map[suc]
        self.edge_number += 1
        self.vertex_list[prc].degree += 1
        self.vertex_list[suc].degree += 1
        self.vertex_adjacency[prc].append(self.vertex_list[suc])

    @abstractmethod
    def get_edges(self, u, v):
        pass

    def get_edge_real_names(self, edge):
        return list(map(lambda x: self.vertex_map_revert[x], edge.vertices))

    def get_arc_real_names(self, edge):
        return tuple(map(lambda x: self.vertex_map_revert[x], edge.vertices))


class UndirectedGraph(Graph):
    """
    Awaits Edge class edges type on input.
    Carries adjacency in both way.
    """
    def __init__(self, vertex_list=None, edge_list=None):
        super().__init__(vertex_list=vertex_list, edge_list=edge_list)

    def add_edge(self, prc=None, suc=None, weight=0):
        """edge = tuple(args: u, v, kwargs: weight)"""
        super().add_edge(prc=prc, suc=suc, weight=weight)
        prc = self.vertex_map[prc]
        suc = self.vertex_map[suc]
        self.vertex_adjacency[suc].append(self.vertex_list[prc])
        self.edge_list.append(self.edge_type(prc=prc, suc=suc, weight=weight))
        self.edge_dict[tuple(sorted([prc, suc]))].append(self.edge_list[-1])

    def get_edges(self, u, v):
        return self.edge_dict[tuple(sorted([u, v]))]


class DirectedGraph(Graph):
    """
    Awaits Arc class edges type on input.
    Additionally carries vertex_adjacency_in - adjacency of vertex by incoming edges.
    Being inherited by Network class.
    """
    def __init__(self, vertex_list=None, edge_list=None):
        super().__init__(vertex_list=vertex_list, edge_list=edge_list)
        self.edge_type = Arc
        self.vertex_adjacency_in = defaultdict(list)

    def add_edge(self, prc=None, suc=None, weight=0):
        """arc = tuple(args: u, v, kwargs: weight)"""
        super().add_edge(prc=prc, suc=suc, weight=weight)
        prc = self.vertex_map[prc]
        suc = self.vertex_map[suc]
        self.edge_list.append(self.edge_type(prc=prc, suc=suc, weight=weight))
        self.edge_dict[tuple([prc, suc])].append(self.edge_list[-1])
        self.vertex_adjacency_in[suc].append(self.vertex_list[prc])
        self.vertex_list[prc].out_half_degree += 1
        self.vertex_list[suc].in_half_degree += 1

    def get_edges(self, u, v):
        return self.edge_dict[(u, v)]
