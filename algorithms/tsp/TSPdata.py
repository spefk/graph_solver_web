import csv
from algorithms.common.functions import dist, get_random_coords
import io


class IncorrectInitialization(Exception):
    pass


class TSPdata:
    def __init__(self, n, sortQ=False, point_to_sort=(0, 0)):
        self.n = -1
        if isinstance(n, int):
            self.n = n
            self.coords = get_random_coords(self.n)

        elif isinstance(n, str):
            if n.endswith('csv'):
                with open(n, newline='') as csvfile:
                    self.coords = [tuple(i) for i in csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)]
                    self.n = len(self.coords)

        elif isinstance(n, list) or isinstance(n, tuple):
            if len(n[0]) == 2:
                self.n = len(n)
                self.coords = [tuple(i) for i in n]
        elif isinstance(n, bytes):
            self.coords = [tuple(i) for i in csv.reader(n.decode('utf-8').splitlines(), quoting=csv.QUOTE_NONNUMERIC)]
            self.n = len(self.coords)
        else:
            raise IncorrectInitialization(r'¯\_(ツ)_/¯')
        if self.n < 3:
            raise IncorrectInitialization()

        if sortQ:
            self.coords.sort(key=lambda x: dist(point_to_sort, x))
        self.update_distance_matrix()

    def __str__(self):
        return "Nodes: {}\nCoords: {}".format(self.n, self.coords)

    def update_distance_matrix(self):
        self.dm = [[dist(self.coords[i], self.coords[j]) for j in range(self.n)] for i in range(self.n)]

    # def write_coords(self, file_name='.csv', path='TSP/Examples'):
    #     if file_name == '.csv':
    #         file_name = str(self.n) + file_name
    #     if not path.endswith('/'):
    #         path = path + '/'
    #     if file_name.endswith('csv'):
    #         with open(path + file_name, 'w', newline='') as csvfile:
    #             reader = csv.writer(csvfile)
    #             reader.writerows(self.coords)
