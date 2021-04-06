from algorithms.tsp.TSPdata import TSPdata, IncorrectInitialization
from algorithms.tsp.TSPmove import MoveRevert, MoveShift
from algorithms.tsp.TSPalgo import LocalSearchBest, LocalSearchFirst, LateAcceptedHillClimbing
from algorithms.tsp.TSPinfo import tsp_info


class TSP:
    def __init__(self, graph, algorithm='Local Search', params=None):
        if params is None:
            params = {'move choice': 'first', 'move types': 'shift, revert', 'initial solution': 'greedy', 'move probability': '0.5, 0.5', 'list size': '10', 'iterations without changes': '100'}

        self.data = TSPdata(graph, params['initial solution'] == 'sorted')
        moves = []
        for move in params['move types'].split(', '):
            if move == 'shift':
                moves.append(MoveShift)
            elif move == 'revert':
                moves.append(MoveRevert)
            else:
                raise IncorrectInitialization


        if algorithm == 'Local Search':
            if params['move choice'] == 'first':
                self.algo = LocalSearchFirst(self.data, moves, construct_method=params['initial solution'])
            elif params['move choice'] == 'best':
                self.algo = LocalSearchBest(self.data, moves, construct_method=params['initial solution'])
            else:
                raise(IncorrectInitialization)

        if algorithm == 'Late Accepted Hill Climbing':
            prob = [float(i) for i in params["move probability"].split(', ')]
            prob = [i / sum(prob) for i in prob]
            if len(prob) != len(moves):
                raise(IncorrectInitialization(f'moves {moves} != prob {prob}'))
            size = int(params['list size'])
            if size < 1:
                raise(IncorrectInitialization('list size'))
            max_iter = int(params['iterations without changes'])
            self.algo = LateAcceptedHillClimbing(self.data, moves, construct_method=params['initial solution'], moves_prop=prob, list_size=size, iterations_without_changes=max_iter)


    # def __init__(self, n, sortQ=False, point_to_sort=(0, 0), moves=None):
    #     if moves is None:
    #         moves = [MoveRevert, MoveShift]
    #     self.data = TSPdata(n, sortQ, point_to_sort)
    #     self.LSB = LocalSearchFirst(self.data, moves)
    #     self.LSF = LocalSearchBest(self.data, moves)
