from time import time
from algorithms.tsp.TSPmove import MoveBestInsertion
from algorithms.common.functions import dist
import random

# TODO 1. move return at first position delta_costs
# TODO 2. initial solutions
# TODO 3. vizualisation
# TODO 4. solution logs
# TODO 5. add max iterations
# TODO 6. add reset solution


class TSPalgo:
    def __init__(self, tsp_data, moves, construct_method="None"):
        self.data = tsp_data
        if construct_method == 'None' or construct_method == 'sorted':
            self.solution = list(range(self.data.n))
        elif construct_method == 'greedy':
            self.solution = MoveBestInsertion(tsp_data).create_solution()
        # elif construct_method == 'sorted':
        #     self.solution = list(range(self.data.n))
        #     self.solution.sort(key=lambda x: dist((0, 0), tsp_data.coords[x]))
        self.costs = self.calculate_costs()
        self.start_costs = self.costs
        self.moves = [move(self.data) for move in moves]
        self.iterations = 1
        self.bound = 1
        self.solutions = [None] * 1000
        self.solutions[1] = self.solution.copy()
        self.total_time = 0
        self.gen = self.generator()

    # def get_initial_solution(self, construct_method=None):
    #     if construct_method is None:
    #         return list(range(self.data.n))
    #     elif construct_method is 'greedy':
    #         solution = []

    def calculate_costs(self):
        costs = 0
        for i in range(self.data.n - 1):
            costs += self.data.dm[self.solution[i]][self.solution[i + 1]]
        return costs + self.data.dm[self.solution[self.data.n - 1]][self.solution[0]]

    def generator(self):
        raise NotImplementedError

    def get_info(self):
        return {'timing': self.total_time, "iteration": self.iterations, "start cost": self.start_costs, "cost": self.costs, "delta": self.start_costs - self.costs, "solution": self.solution}

    def solve(self, n):
        if n < 0:
            self.iterations += max(n, - self.iterations + 1)
            self.solution = self.solutions[self.iterations].copy()
            self.costs = self.calculate_costs()
            return None
        if self.iterations < self.bound:
            delta = self.bound - self.iterations
            if delta >= n:
                self.iterations += n
                n = 0
            else:
                self.iterations += delta
                n -= delta
            self.solution = self.solutions[self.iterations].copy()
            self.costs = self.calculate_costs()
        for _ in range(n):
            try:
                t = time()
                next(self.gen)
                self.total_time += time() - t
            except StopIteration:
                break

            self.iterations += 1
            self.bound = self.iterations
            if self.iterations >= len(self.solutions):
                self.solutions += [None] * 1000
            self.solutions[self.iterations] = self.solution.copy()

    # def solve(self):
    #     self.iterations = 0
    #     for _ in self.generator():
    #         self.iterations += 1
    #         continue

    def solve_info(self):
        t = time()
        costs = self.costs
        self.solve()
        print('Timing: {}'.format(time() - t))
        print('Iter:   {}'.format(self.iterations))
        print('Before: {}'.format(costs))
        print('After:  {}'.format(self.costs))
        print('Delta:  {}\n'.format(costs - self.costs))


class LocalSearchBest(TSPalgo):
    def generator(self):
        while True:
            self.iterations += 1
            moves_cost = [move.best(self.solution) for move in self.moves]
            best_move = self.moves[0]
            best_move_cost = moves_cost[0]
            if len(self.moves) > 1:
                for i in range(1, len(self.moves)):
                    if moves_cost[i][2] < best_move_cost[2]:
                        best_move = self.moves[i]
                        best_move_cost = moves_cost[i]
            if best_move_cost[2] >= 0:
                return None
            else:
                best_move.move(self.solution, *best_move_cost)
                self.costs += best_move_cost[2]
                yield best_move_cost[2]


class LocalSearchFirst(TSPalgo):
    def generator(self):
        while True:
            for move in self.moves:
                last_move = move
                last_move_cost = move.first(self.solution)
                if last_move_cost[2] < 0:
                    break
            if last_move_cost[2] < 0:
                last_move.move(self.solution, *last_move_cost)
                self.costs += last_move_cost[2]
                yield last_move_cost[2]
            else:
                return None


class LateAcceptedHillClimbing(TSPalgo):
    def __init__(self, tsp_data, moves, construct_method="None", moves_prop=None, list_size=10, iterations_without_changes=100):
        super().__init__(tsp_data, moves, construct_method="None")
        if moves_prop is None:
            self.moves_prop = [1 / len(moves)] * len(moves)
        else:
            self.moves_prop = moves_prop
        self.accumulated_prop = []
        acc = 0
        for i in self.moves_prop:
            acc += i
            self.accumulated_prop.append(acc)
        self.size = list_size
        self.states = [self.costs] * self.size
        self.current_state = 0
        self.no_changes = 0
        self.max = iterations_without_changes

    def get_move(self):
        rnd = random.random()
        for i in range(len(self.accumulated_prop)):
            if self.accumulated_prop[i] >= rnd:
                return self.moves[i]
        return self.moves[-1]

    def generator(self):
        while self.no_changes <= self.max:
            print(self.no_changes)
            move = self.get_move()
            random_move_cost = move.random(self.solution)
            # print(f"delta {random_move_cost[2]}, ")
            if random_move_cost[2] < 0 or (self.costs + random_move_cost[2]) <= self.states[self.current_state]:
                move.move(self.solution, *random_move_cost)
                self.costs += random_move_cost[2]
                self.states[self.current_state] = self.costs
                self.current_state = (self.current_state + 1) % self.size
                yield random_move_cost[2]
                self.no_changes = 0
            else:
                self.no_changes += 1
                continue
