from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    graphs_number = db.Column(db.Integer)

    graphs = db.relationship('GraphData', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.graphs_number = 0

    def __repr__(self):
        return f"User(id: '{self.id}', username: '{self.username}')"


class GraphData(db.Model):
    __tablename__ = 'graph_data'

    id = db.Column(db.Integer, primary_key=True)

    graph_name = db.Column(db.String(60), nullable=False)
    graph_filename = db.Column(db.String(60), nullable=False)
    graph_data = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    algorithms_data = db.relationship('AlgorithmData', backref='graph', lazy=True)

    def __init__(self, user_id=None, graph_name=None, graph_filename=None,
                 graph_data=None, directed=None, coordinates=None):
        self.user_id = user_id
        self.graph_name = graph_name
        self.graph_filename = graph_filename
        self.graph_data = graph_data
        self.directed = directed
        self.coordinates = coordinates

    def columns_rerp(self):
        return [self.id, self.graph_name, self.graph_filename]

    def __repr__(self):
        return f"Graph(id: {self.id}, user_id: {self.user_id}," \
               f"graph_name: {self.graph_name}, filename: {self.graph_filename})"


class AlgorithmData(db.Model):
    __tablename__ = 'algorithm_data'

    id = db.Column(db.Integer, primary_key=True)

    graph_id = db.Column(db.Integer, db.ForeignKey('graph_data.id'), nullable=False)

    algorithm = db.Column(db.String(20), unique=False, nullable=False)
    solution = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, graph_id, algorithm, solution):
        self.graph_id = graph_id
        self.algorithm = algorithm
        self.solution = solution

    def __repr__(self):
        return f"AlgorithmData('{self.id}', '{self.graph_id}', '{self.algorithm}'," \
               f"'{self.images_folder}', '{self.result_path}')"
