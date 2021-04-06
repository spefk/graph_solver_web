from algorithms.graphs.graph_class import *
from algorithms.graphs.graph_objects_classes import *


class NetworkArc(Arc):
    def __init__(self, prc=None, suc=None, weight=0, capacity=float('inf')):
        super().__init__(prc, suc)
        self.capacity = capacity
        self.cost = weight
        self.flow = 0
        self.direction = 1

    def reset(self):
        self.flow = 0
        self.direction = 1

    def __repr__(self):
        return f'({self.vertices}, capacity: {self.capacity} current flow: {self.flow}'


class Network(DirectedGraph):

    def __init__(self, vertex_list=None, edge_list=None):
        super().__init__(vertex_list=vertex_list, edge_list=edge_list)
        self.edge_type = NetworkArc
        self.s = None
        self.t = None
        self.flow = 0

    def add_edge(self, prc=None, suc=None, weight=0, capacity=float('inf')):
        super().add_edge(prc=prc, suc=suc, weight=weight)
        prc = self.vertex_map[prc]
        suc = self.vertex_map[suc]
        self.edge_dict[tuple([prc, suc])][-1].capacity = capacity

    @staticmethod
    def reset_arc(arc):
        arc.flow = 0
        arc.direction = 1

    def reset_network(self):
        self.flow = 0
        for arc in self.edge_list:
            self.reset_arc(arc)
