from algorithms.graphs.graph_network_class import *


class MaxFlowFinder:

    def __init__(self, network: Network):
        self.network = network
        self.visited = []
        self.solutions = []
        self.solutions_value = []

    def dfs_ford_fulkerson(self, prc, t, delta=float('inf')):
        self.visited[prc] = True

        # Forth stream
        for suc in self.network.vertex_adjacency[prc]:
            suc = suc.name
            if not self.visited[suc]:
                for cur_arc in self.network.edge_dict[tuple([prc, suc])]:
                    cur_delta = min(delta, cur_arc.capacity - cur_arc.flow)
                    if cur_delta > 0:
                        if suc is not t:
                            cur_delta = self.dfs_ford_fulkerson(suc, t, delta=cur_delta)
                        if cur_delta > 0:
                            cur_arc.flow += cur_delta
                            return cur_delta

        # Back stream
        for suc in self.network.vertex_adjacency_in[prc]:
            suc = suc.name
            if not self.visited[suc]:
                for cur_arc in self.network.edge_dict[tuple([suc, prc])]:
                    cur_delta = min(delta, cur_arc.flow)
                    if cur_delta > 0:
                        if suc is not t:
                            cur_delta = self.dfs_ford_fulkerson(suc, t, delta=cur_delta)
                        if cur_delta > 0:
                            cur_arc.flow -= cur_delta
                            return cur_delta

        # no possibility of stream with delta>0
        return 0

    def collect_arc_data(self):
        return [(self.network.get_arc_real_names(x), x.flow, x.capacity) for x in self.network.edge_list]

    def ford_fulkerson(self, s, t):
        """Finds maximal-flow in graph with integer capacities."""

        self.network.s = self.network.vertex_map[s]
        self.network.t = self.network.vertex_map[t]
        self.solutions = [self.collect_arc_data()]
        self.solutions_value = [self.network.flow]

        while True:
            self.visited = [False] * self.network.vertex_number
            delta = self.dfs_ford_fulkerson(self.network.s, self.network.t, delta=float('inf'))
            if delta <= 0:
                break
            self.network.flow += delta
            self.solutions.append(self.collect_arc_data())
            self.solutions_value.append(self.network.flow)
        self.visited = []
        return self.network.flow
