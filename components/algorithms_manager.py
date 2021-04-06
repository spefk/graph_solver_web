from algorithms.graphs.graph_class import Graph, UndirectedGraph, DirectedGraph
from algorithms.graphs.graph_network_class import Network
from algorithms.apsp.shortest_path_class import ShortestPathFinder
from algorithms.flows.maximal_flow_class import MaxFlowFinder


class GraphBuilder:
    def __init__(self, dbHandler):
        self.dbHandler = dbHandler

    def get_graph_file(self, graph_id):
        return self.dbHandler.read_graph_by_id(graph_id)

    @staticmethod
    def add_edge(graph, line):

        line = tuple(map(int, line.strip().split()))
        if type(graph) is UndirectedGraph or type(graph) == DirectedGraph:
            graph.add_edge(prc=line[0], suc=line[1], weight=line[2])
        elif type(graph) is Network:
            graph.add_edge(prc=line[0], suc=line[1], capacity=line[2])
        else:
            raise Exception('UnknownGraphClass')

    def get_graph(self, graph_id):

        graph_file = self.get_graph_file(graph_id)
        data_type = graph_file[0].strip()
        graph_type = graph_file[1].strip()

        if graph_type == b'undirected':
            graph = UndirectedGraph()
        elif graph_type == b'directed':
            graph = DirectedGraph()
        elif graph_type == b'network':
            graph = Network()
        else:
            raise Exception('UnknownGraphType')

        if data_type == b'edges':
            for i in range(2, len(graph_file)):
                self.add_edge(graph, graph_file[i])
        elif data_type == b'coordinates':
            pass
        else:
            raise Exception('UnknownGraphDataType')

        return graph


class AlgorithmManager:
    def __init__(self, dbHandler):
        self.dbHandler = dbHandler
        self.graph_builder = GraphBuilder(self.dbHandler)

    def go_tsp(self, graph_id):
        pass

    def go_apsp(self, graph_id, algorithm_mode='1_to_all', s=0, t=1):
        if not isinstance(graph_id, Graph):
            graph = self.graph_builder.get_graph(graph_id)
        else:
            graph = graph_id
        spFinder = ShortestPathFinder(graph)
        if algorithm_mode == '1_to_1':
            return spFinder.sp_pair_path(int(s), int(t)), spFinder.sp_pair_distances(int(s), int(t))
        elif algorithm_mode == "1_to_all":
            return spFinder.sp_one_to_all(int(s)), None
        elif algorithm_mode == "all_to_all":
            return spFinder.sp_all_to_all(), None
        else:
            raise Exception('WrongAlgorithmMode')

    def go_max_flow(self, graph_id, s, t):
        if not isinstance(graph_id, Graph):
            graph = self.graph_builder.get_graph(graph_id)
        else:
            graph = graph_id
        maxFlow = MaxFlowFinder(graph)
        maxFlow.ford_fulkerson(s, t)
        return maxFlow

# Functions are to return instance of Class of chosen algorithm?
