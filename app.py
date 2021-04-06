import io
import imageio
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash
from werkzeug.datastructures import CombinedMultiDict
from components.forms import RegisterForm, LoginForm, UploadGraphForm, TSPForm, MaxFlowForm, APSPForm
from components.database_models import db, User
from components.database_handler.database_handler import DatabaseHandler
from components.algorithms_manager import AlgorithmManager
from algorithms.tsp.TSPclass import TSP, tsp_info
from algorithms.graphs.graph_visualization import GraphVisualizer
from algorithms.apsp.shortest_path_info import apsp_info
from algorithms.flows.maximal_flow_info import flow_info
from components.tests.test_db import test_db_update, test_db_create

app = Flask(__name__)
Bootstrap(app)

postgres_url = 'postgresql://team3:nWYUG2pd@/team3_db?host=rc1a-4ot4njdg61e0mtjq.mdb.yandexcloud.net&port=6432'
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max-limit.
app.config['SECRET_KEY'] = 'secret_wazzuuup'

db.app = app
db.init_app(app)
dbHandler = DatabaseHandler(db)

login_manager = LoginManager()
login_manager.init_app(app)

algoManager = AlgorithmManager(dbHandler)

current_users_data = defaultdict(lambda: {"step": 1, "max step": 4, "graph": None, "graph name": None, "algo": None,
                                          "algo index": 0, "params": None, "solver": None, "step size": 10, "info": {},
                                          "visualizer": None, "solution": [], 'apsp_type': None, 'apsp_vert_names': [],
                                          'apsp_distance': None})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET'])
@app.route("/?message=<message>", methods=['GET'])
def index(message=None):
    if not current_user.is_authenticated:
        return login()
    return render_template("index.html", message=message)


@app.route("/login", methods=['GET', 'POST'])
@app.route("/login/?message=<message>", methods=['GET', 'POST'])
def login(message=None):
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index', message='Login was successful.'))
            return redirect(url_for('login', message='Password is incorrect.'))
        return redirect(url_for('login', message='Username doesn\'t exist.'))
    return render_template("login.html", message=message, form=form)


@app.route("/reg_form", methods=['GET', 'POST'])
def reg_form():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        dbHandler.upload_user(form.username.data, form.password.data)
        return redirect(url_for('login', message='Registration was successful.'))
    return render_template("reg_form.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login', message='Logout successful.'))


@app.route("/help", methods=['GET', 'POST'])
@login_required
def help_page():
    return render_template("help.html")


@app.route("/user_profile", methods=['GET', 'POST'])
@app.route("/user_profile/?message=<message>", methods=['GET', 'POST'])
@login_required
def user_profile(message=None):
    graph_list = dbHandler.get_user_graphs()
    form = UploadGraphForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and form.validate_on_submit():
        dbHandler.upload_graph_data(form.graph.data, form.graph_name.data)
        return redirect(url_for('user_profile', graph_list=graph_list, form=form, message='Graph uploaded.'))
    return render_template("user_profile.html", graph_list=graph_list, form=form, message=message)


@app.route("/tsp", methods=['GET', 'POST'])
@login_required
def tsp():
    data = current_users_data[current_user.id]
    form = TSPForm(CombinedMultiDict((request.files, request.form)))
    available_graphs = dbHandler.get_user_graphs_choicelist()
    form.select_graph.choices = available_graphs
    if data['step'] == 3 and data['graph name'] is None:
        data['step'] = 1
    if data['step'] == data['max step'] and data['solver'] is None:
        data['step'] = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'graph':
            if form.select_graph.data != '...':
                data["graph"] = dbHandler.get_graph_by_id(form.select_graph.data)
                data["graph name"] = str(data["graph"])
                data["graph"] = data["graph"].graph_data
                data["step"] += 1
            else:
                file = form.downloaded_graph.data
                if file is not None:
                    graph_id = dbHandler.upload_graph_data(file, file.filename)
                    data["graph"] = dbHandler.get_graph_by_id(graph_id)
                    data["graph name"] = str(data["graph"])
                    data["graph"] = data["graph"].graph_data
                    data["step"] += 1

        elif request.form['submit_button'] == 'algorithm' and request.form.get("algo") is not None:
            data["algo index"] = int(request.form.get("algo"))
            data["step"] += 1

        elif request.form['submit_button'] == 'params' and data["step"] == 3:
            data["params"] = dict((param['name'], request.form[param['name']])
                                  for param in tsp_info[data["algo index"]]["parameters"])
            data["step"] += 1
            data["algo"] = tsp_info[data["algo index"]]['name']
            print(data["algo"])
            print(data["params"])
            data["solver"] = TSP(data["graph"], algorithm=data["algo"], params=data["params"])
            data["info"] = data["solver"].algo.get_info()
            data["visualizer"] = GraphVisualizer(data["solver"].data.coords)

        elif request.form['submit_button'] == 'next':
            try:
                data['step size'] = max(1, int(request.form['step size']))
            except:
                pass
            data["solver"].algo.solve(data['step size'])
            data["info"] = data["solver"].algo.get_info()

        elif request.form['submit_button'] == 'prev':
            try:
                data['step size'] = max(1, int(request.form['step size']))
            except:
                pass
            data["solver"].algo.solve(-data['step size'])
            data["info"] = data["solver"].algo.get_info()

        elif request.form['submit_button'] == 'animation':
            try:
                data['step size'] = max(1, int(request.form['step size']))
            except:
                pass

            return render_template("tsp.html", title='TSP', algorithms_info=tsp_info,
                                   form=form, data=data, animateQ=True)

        elif request.form['submit_button'] == 'reset':
            data["step"] = 1
            data["graph"] = None
            data["graph name"] = None
            data["algo"] = None
            data["algo index"] = 0
            data["solver"] = None
        elif request.form['submit_button'] == 'reset algo':
            data["step"] = 2
        elif request.form['submit_button'] == 'reset params':
            data["step"] = 3

    return render_template("tsp.html", title='TSP', algorithms_info=tsp_info, form=form, data=data, animateQ=False)


@app.route('/tsp_img2/<int:iteration>')
def tsp_img(iteration):
    data = current_users_data[current_user.id]
    data["visualizer"].update_edges_form_sequence_of_nodes(data["solver"].algo.solutions[iteration])
    img = data["visualizer"].visualize_graph(nodes_labels=True, nodes_options={'node_size': 30, 'node_color': 'white'},
                                             edges_options={'edge_color': '#191919'})

    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/tsp/animate/<int:step>')
def tsp_anim(step):
    def get_images(cur_tsp, visualizer):
        for i in range(1, cur_tsp.algo.iterations + 1, step):
            print(f"{i}/{cur_tsp.algo.iterations}")
            visualizer.update_edges_form_sequence_of_nodes(cur_tsp.algo.solutions[i])
            yield imageio.imread(visualizer.visualize_graph(nodes_labels=True,
                                                            nodes_options={'node_size': 30, 'node_color': 'white'}),
                                 format='png')

        visualizer.update_edges_form_sequence_of_nodes(cur_tsp.algo.solutions[cur_tsp.algo.iterations])
        last_img = imageio.imread(visualizer.visualize_graph(nodes_labels=True,
                                                             nodes_options={'node_size': 30, 'node_color': 'white'}),
                                  format='png')
        for _ in range(20):
            yield last_img

    data = current_users_data[current_user.id]
    anim = io.BytesIO()
    imageio.mimsave(anim, get_images(data["solver"], data["visualizer"]), format='gif')
    anim.seek(0)
    return send_file(anim, mimetype='image/gif', cache_timeout=0)


@app.route("/apsp", methods=['GET', 'POST'])
@login_required
def apsp():
    data = current_users_data[current_user.id]
    image_case = False
    form = APSPForm(CombinedMultiDict((request.files, request.form)))
    form.select_graph.choices = dbHandler.get_user_graphs_choicelist()
    form.algorithm_mode.choices = [('...', '...'), ('1_to_1', '1_to_1'),
                                   ('all_to_all', 'all_to_all'), ('1_to_all', '1_to_all')]
    if request.method == 'POST' and form.validate_on_submit():
        graph = algoManager.graph_builder.get_graph(form.select_graph.data)
        data['solution'], data['apsp_distance'] =\
            algoManager.go_apsp(graph, form.algorithm_mode.data, form.s.data, form.t.data)
        data['apsp_type'] = form.algorithm_mode.data
        data['apsp_vert_names'] = [v.name for v in graph.vertex_list]
        data['visualizer'] = GraphVisualizer(graph, directedQ=True)
        image_case = form.algorithm_mode.data
    return render_template("apsp.html", title='APSP', algorithms_info=apsp_info,
                           form=form, image_case=image_case, solution=data['solution'],
                           vert_names=data['apsp_vert_names'], distance=data['apsp_distance'])


@app.route("/apsp_img", methods=['GET', 'POST'])
@login_required
def apsp_img():
    data = current_users_data[current_user.id]
    if data['apsp_type'] == '1_to_1':
        img = data["visualizer"].highlight_path(path=data['solution'])
    else:
        img = data["visualizer"].highlight_path(path=[])
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route("/flows", methods=['GET', 'POST'])
@login_required
def flows():
    data = current_users_data[current_user.id]
    image_case = False
    form = MaxFlowForm(CombinedMultiDict((request.files, request.form)))
    form.select_graph.choices = dbHandler.get_user_graphs_choicelist()
    form.algorithm.choices = [('...', '...'), ('ff', 'Ford Fulkerson')]
    if request.method == 'POST':
        if request.form['submit_button'] == 'prev':
            image_case = True
            data['step size'] = max(1, int(request.form['step size']))
            print(data['step size'])
            print(data['step'])
            data['step'] = max(data['step'] - data['step size'], 0)
        elif request.form['submit_button'] == 'next':
            image_case = True
            data['step size'] = max(1, int(request.form['step size']))
            print(data['step size'])
            print(data['step'])
            data['step'] = min(data['step'] + data['step size'], len(data['solver'].solutions) - 1)
        elif form.validate_on_submit():
            image_case = True
            graph = algoManager.graph_builder.get_graph(form.select_graph.data)
            data['step'] = 0
            data['step size'] = 1
            data['solver'] = algoManager.go_max_flow(graph, form.s.data, form.t.data)
            data['visualizer'] = GraphVisualizer(graph, networkQ=True)
    return render_template("flows.html", title='Maximal Flow', algorithms_info=flow_info,
                           form=form, data=data, image_case=image_case)


@app.route("/flows_img/<it>", methods=['GET', 'POST'])
@login_required
def flows_img(it):
    data = current_users_data[current_user.id]
    data["visualizer"].update_network_arcs(data["solver"].solutions[int(it)])
    img = data["visualizer"].visualize_graph()
    return send_file(img, mimetype='image/png', cache_timeout=0)


if __name__ == '__main__':
    # test_db_create(dbHandler)
    # test_db_update(db)
    app.debug = True
    app.run()
