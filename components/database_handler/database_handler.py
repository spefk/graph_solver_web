import os.path
from io import BytesIO
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from components.database_models import User, GraphData, AlgorithmData


class DatabaseHandler:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def upload_user(self, username, password):
        hash_pass = generate_password_hash(password)
        user = User(username, hash_pass)
        self.db.session.add(user)
        self.db.session.commit()

    def upload_graph_data(self, file, graph_name):
        current_user.graphs_number += 1
        graph_filename = file.filename
        graph_data = file.read()
        if graph_name == '':
            graph_name = graph_filename
        graph = GraphData(user_id=current_user.id, graph_name=graph_name,
                          graph_data=graph_data, graph_filename=graph_filename)
        print(f'Graph saved. filename: {graph_filename}')
        self.db.session.add(graph)
        self.db.session.commit()
        return graph.id

    def upload_algorithm_data(self):
        pass

    @staticmethod
    def get_graph_by_id(graph_id):
        return GraphData.query.filter_by(id=graph_id).first()

    def get_user_graphs(self):
        return self.db.session.query(GraphData).filter(GraphData.user_id == current_user.id).all()

    def get_graph_algorithms(self, graph_id):
        return self.db.session.query(AlgorithmData).filter(AlgorithmData.graph_id == graph_id).all()

    def read_graph_by_id(self, graph_id):
        graph = self.get_graph_by_id(graph_id)
        out = [x for x in BytesIO(graph.graph_data).readlines()]
        return out

    def get_user_graphs_choicelist(self):
        return [('...', '...')] + [(user_graph.id, user_graph.graph_name)
                                   for user_graph in self.get_user_graphs()]
