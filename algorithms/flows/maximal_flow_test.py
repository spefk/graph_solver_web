from algorithms.flows.maximal_flow_class import *
from algorithms.graphs.graph_visualization import GraphVisualizer

"""
    Testing samples and testing algorithms run.
"""

if __name__ == '__main__':
    network = Network()
    network.add_edge(prc=1, suc=2, capacity=10)
    network.add_edge(prc=2, suc=3, capacity=10)
    network.add_edge(prc=3, suc=4, capacity=20)
    network.add_edge(prc=1, suc=5, capacity=20)
    network.add_edge(prc=5, suc=3, capacity=20)
    network.add_edge(prc=2, suc=4, capacity=10)

    mff = MaxFlowFinder(network)
    mff.ford_fulkerson(1, 4)

    graph_vis = GraphVisualizer(network, networkQ=True, directedQ=True)
    graph_vis.visualize_graph()
