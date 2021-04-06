from random import uniform


def dist(x, y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5


def get_random_coords(n, x_range=None, y_range=None):
    if y_range is None:
        y_range = [0, 100]
    if x_range is None:
        x_range = [0, 100]
    return [(uniform(x_range[0], x_range[1]), uniform(y_range[0], y_range[1])) for _ in range(n)]


