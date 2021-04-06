from components.database_models import User, GraphData, AlgorithmData
from components.database_handler.database_handler import DatabaseHandler


def test_db_create(dbHandler: DatabaseHandler):
    dbHandler.db.drop_all()
    dbHandler.db.create_all()

    dbHandler.upload_user("spefk", "123123")
    dbHandler.upload_user("sheldon", "111111")


def test_db_update(db):
    db.session.add(User(0, 'test_user_0', 'pass'))
    db.session.add(GraphData(1, 0, "tmp1"))
    db.session.add(GraphData(2, 0, "tmp2"))
    db.session.add(AlgorithmData(1, 1, 'gr1_1', 'res1', 'im1'))
    db.session.add(AlgorithmData(2, 2, 'gr2_1', 'res2', 'im1'))
    db.session.add(AlgorithmData(3, 2, 'gr2_2', 'res3', 'im3'))
    db.session.commit()

    print(db.session.execute("SELECT results_folder FROM algorithm_data WHERE graph_id = :graph_id",
                             {'graph_id': 1}).fetchall())
    print(db.session.execute("SELECT results_folder FROM algorithm_data WHERE graph_id = :graph_id",
                             {'graph_id': 2}).fetchall())
    print(db.session.execute("SELECT DISTINCT  results_folder FROM algorithm_data, graph_data WHERE user_id = :user_id",
                             {'user_id': 0}).fetchall())
    print(db.session.execute("SELECT DISTINCT  results_folder FROM algorithm_data, graph_data WHERE user_id = :user_id",
                             {'user_id': 1}).fetchall())

    print('___1___')
    for x in AlgorithmData.query.filter(AlgorithmData.graph_id == 1).all():
        print(x)

    print('___2___')
    for x in db.session.query(AlgorithmData).filter(AlgorithmData.graph_id == 2).all():
        print(x)

    print('___3___')
    for x in db.session.query(AlgorithmData).join(GraphData).filter(GraphData.id == 2).all():
        print(x)

    print('___4___')
    for x in db.session.query(AlgorithmData).join(GraphData).\
            with_entities(AlgorithmData.images_folder, AlgorithmData.results_folder).\
            filter(GraphData.id == 2).all():
        print(x)
