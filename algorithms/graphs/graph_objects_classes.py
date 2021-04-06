class Vertex:
    def __init__(self, name: int, tag='', coords=(0, 0)):
        if type(name) is not int:
            raise Exception('UnexpectedVertexNameType')
        self.name = name
        self.tag = tag
        self.coords = coords
        self.degree = 0
        self.in_half_degree = 0
        self.out_half_degree = 0

    def __repr__(self):
        return f"{self.name}"


class Edge:
    def __init__(self, prc=None, suc=None, weight=0.):
        self.vertices = [prc, suc]
        self.weight = weight

    def __repr__(self):
        return f"{self.vertices}"


class Arc:
    def __init__(self, prc=None, suc=None, weight=0):
        self.vertices = tuple([prc, suc])
        self.weight = weight

    def __repr__(self):
        return f"{self.vertices}"
