## Graph Solver
Web interface for solving different problems on graphs. (training project)

*temporary broken due to disabling access to postgresql database*

#### Features

- Login system (flask_login)
- Database storage (PostgreSQL)
- Graph classes and algorithms (for tsp, apsp, max-flow)

#### Used packages

- Flask
- SQLAlchemy
- WTForms
- NetworkX (for visualisation)
- werkzeug (passford hashing)
- etc.

#### Screenshots

TSP interface:
![tsp](https://github.com/spefk/graph_solver_web/blob/main/static/screenshots/tsp_works.png)

APSP interface:
![apsp](https://github.com/spefk/graph_solver_web/blob/main/static/screenshots/apsp_1_to_1_works.png)

Info page:
![info](https://github.com/spefk/graph_solver_web/blob/main/static/screenshots/help_page.png)