import matplotlib
import imageio
from algorithms.tsp.TSPclass import TSP
from flask import Flask, send_file
from algorithms.graphs.graph_visualization import GraphVisualizer
import io

app = Flask(__name__)


tsp = TSP(30, algorithm='Late Accepted Hill Climbing')
tsp.algo.solve(50)


visualizer = GraphVisualizer(tsp.data.coords, base_color='#191919')

# Рисует, если не стоит matplotlib.use('Agg') в algorithms.graphs.graph_visualization
visualizer.update_edges_form_sequence_of_nodes(tsp.algo.solutions[1])
visualizer.visualize_graph(nodes_labels=True, nodes_options={'node_size': 30, 'node_color': 'white'})


def get_images(tsp, visualizer):
    for i in range(1, tsp.algo.bound + 1):
        try:
            visualizer.update_edges_form_sequence_of_nodes(tsp.algo.solutions[i])
            yield imageio.imread(visualizer.visualize_graph(nodes_labels=True, nodes_options={'node_size': 30, 'node_color': 'white'}), format='png')
        except:
            break


anim = io.BytesIO()
# imageio.mimsave(anim, get_images(tsp, visualizer), format='gif')
anim.seek(0)


@app.route('/img/<int:iteration>')
def get_img(iteration):
    visualizer.update_edges_form_sequence_of_nodes(tsp.algo.solutions[iteration])
    img = visualizer.visualize_graph(nodes_labels=True, nodes_options={'node_size': 30, 'node_color': 'white'})
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/anim')
def animate():
    return send_file(anim, mimetype='image/gif', cache_timeout=0)


app.debug = True

if matplotlib.get_backend() == ' agg':
    app.run()
