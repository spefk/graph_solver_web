import matplotlib
import matplotlib.pyplot as plt
import io
import networkx as nx
from algorithms.graphs.graph_class import Graph

matplotlib.use('Agg')


class GraphVisualizer:

    def __init__(self, graph, networkQ=False, directedQ=False,
                 base_color='blue', highlight_color='red'):

        self.base_color = base_color
        self.highlight_color = highlight_color
        self.pos = None  # for nodes with coordinates

        if isinstance(graph, Graph):

            self.networkQ = networkQ
            self.directedQ = directedQ
            self.graph = None
            self.options = None

            if networkQ:
                self.edge_label_type = 'capacity'
                self.network_arcs_weights = {graph.get_arc_real_names(arc): float(arc.flow/arc.capacity)
                                             for arc in graph.edge_list}
            else:
                self.edge_label_type = 'weight'

            self.get_graph(graph)

        elif isinstance(graph, nx.Graph):

            self.graph = graph

        elif isinstance(graph, list) and all(map(lambda x: len(x) == 2, graph)):

            self.graph = nx.Graph()
            for i in range(len(graph)):
                self.graph.add_node(i, coord=graph[i])
            self.pos = nx.get_node_attributes(self.graph, 'coord')

    # builds nx graph from instance of Graph
    def get_graph(self, graph):

        if self.directedQ or self.networkQ:
            self.graph = nx.DiGraph()
            self.options = {'arrows': True, 'width': 2, 'arrowstyle': '-|>', 'arrowsize': 12}
        else:
            self.graph = nx.Graph()
            self.options = {'width': 2}

        for edge in graph.edge_list:
            self.graph.add_edge(*graph.get_arc_real_names(edge), weight=eval(f'edge.{self.edge_label_type}'))

    def delete_all_edges(self):
        self.graph.remove_edges_from(list(self.graph.edges()))

    def add_edges(self, edge_list):
        self.graph.add_edges_from(edge_list)

    def add_edges_network(self, edges_list):
        for edge in edges_list:
            self.graph.add_edge(edge[0][0], edge[0][1], weight=float(edge[1]/edge[2]))

    def update_edges(self, edges_list):
        self.delete_all_edges()
        self.add_edges(edges_list)

    def update_network_arcs(self, net_arc_list):
        self.delete_all_edges()
        self.add_edges_network(net_arc_list)
        self.network_arcs_weights = {arc[0]: float(arc[1]/arc[2])
                                     for arc in net_arc_list}

    def update_edges_form_sequence_of_nodes(self, nodes):
        n = len(nodes)
        edges_list = [(nodes[i - 1], nodes[i % n]) for i in range(1, n + 1)]
        self.update_edges(edges_list)

    def highlight_path(self, path=None):
        if path is None:
            path = []
        return self.visualize_graph(highlight_edges=[(path[i], path[i + 1]) for i in range(len(path) - 1)])

    def visualize_graph(self, highlight_vertices=None, highlight_edges=None, nodes_options=None,
                        edges_options=None, nodes_labels=False):
        if highlight_vertices is None:
            highlight_vertices = []
        if highlight_edges is None:
            highlight_edges = []
        if nodes_options is None:
            nodes_options = {}
        if edges_options is None:
            edges_options = {}

        plt.clf()
        if self.pos is None:
            if self.networkQ:
                edge_colors = [self.network_arcs_weights[arc] for arc in self.graph.edges]
            else:
                edge_colors = [self.highlight_color if edge in highlight_edges else self.base_color
                               for edge in self.graph.edges]
            edge_weights = nx.get_edge_attributes(self.graph, 'weight')

            nx.draw_networkx(self.graph, nx.circular_layout(self.graph), edge_color=edge_colors,
                             edge_cmap=plt.get_cmap('Blues'), **self.options)
            nx.draw_networkx_edge_labels(self.graph, nx.circular_layout(self.graph), edge_labels=edge_weights)
        else:
            nx.draw_networkx_nodes(self.graph, self.pos, **nodes_options)
            nx.draw_networkx_edges(self.graph, self.pos, **edges_options)
            if nodes_labels:
                labels = {i: str(i) for i in self.graph.nodes}
                nx.draw_networkx_labels(self.graph, self.pos, labels, font_size=8)

        if matplotlib.get_backend() == 'agg':
            img = io.BytesIO()
            plt.savefig(img)
            img.seek(0)
            plt.clf()
            return img
        else:
            plt.show()
