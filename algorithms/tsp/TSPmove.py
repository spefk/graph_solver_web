import random


class TSPmove:
    def __init__(self, tsp_data):
        self.data = tsp_data

    def _get_arc_cost_in_solution(self, solution, start, end):
        if end == -1:
            end = self.data.n - 1
        elif end == self.data.n:
            end = 0

        if start == -1:
            start = self.data.n - 1
        elif start == self.data.n:
            start = 0
        if start == end:
            return 0
        else:
            return self.data.dm[solution[start]][solution[end]]


class MoveBestInsertion(TSPmove):
    def cost(self, solution, node, to_pos):
        delta_costs = self.data.dm[node][solution[to_pos]]
        if to_pos == 0:
            delta_costs += self.data.dm[solution[-1]][node]
        else:
            delta_costs += self.data.dm[solution[to_pos - 1]][node]
        return delta_costs

    def best(self, solution, node):
        best_to_pos, min_cost = 0, self.cost(solution, node, 0)
        for to_pos in range(1, len(solution)):
            cost = self.cost(solution, node, to_pos)
            if cost < min_cost:
                best_to_pos, min_cost = to_pos, cost

        return solution, node, best_to_pos, min_cost

    def move(self, solution, node, to_pos, delta_cost=0):
        solution.insert(to_pos, node)
        return delta_cost

    def create_solution(self):
        solution = [0]
        for node in range(1, self.data.n):
            self.move(*self.best(solution, node))
        return solution


class MoveShift(TSPmove):
    def cost(self, solution, from_pos, to_pos):
        if from_pos == 0 and to_pos == self.data.n - 1 or from_pos == self.data.n - 1 and to_pos == 0:
            return 0
        if from_pos > to_pos:
            delta_costs = \
                - self._get_arc_cost_in_solution(solution, from_pos - 1, from_pos) \
                - self._get_arc_cost_in_solution(solution, from_pos, from_pos + 1) \
                - self._get_arc_cost_in_solution(solution, to_pos - 1, to_pos) \
                + self._get_arc_cost_in_solution(solution, to_pos - 1, from_pos) \
                + self._get_arc_cost_in_solution(solution, from_pos, to_pos) \
                + self._get_arc_cost_in_solution(solution, from_pos - 1, from_pos + 1)
        else:
            delta_costs = \
                - self._get_arc_cost_in_solution(solution, from_pos - 1, from_pos) \
                - self._get_arc_cost_in_solution(solution, from_pos, from_pos + 1) \
                - self._get_arc_cost_in_solution(solution, to_pos, to_pos + 1) \
                + self._get_arc_cost_in_solution(solution, to_pos, from_pos) \
                + self._get_arc_cost_in_solution(solution, from_pos, to_pos + 1) \
                + self._get_arc_cost_in_solution(solution, from_pos - 1, from_pos + 1)
        return delta_costs

    def random(self, solution):
        i = random.randint(0, self.data.n - 1)
        j = random.randint(0, self.data.n - 2)
        if j >= i:
            j += 1
        return (i, j, self.cost(solution, i, j))

    def generator(self, solution):
        for i in range(self.data.n):
            for j in range(self.data.n):
                if i == j:
                    continue
                else:
                    yield (i, j, self.cost(solution, i, j))

    def random_generator(self, solution):
        i_list = list(range(self.data.n))
        random.shuffle(i_list)
        for i in i_list:
            j_list = list(range(self.data.n))
            random.shuffle(j_list)
            for j in j_list:
                if i == j:
                    continue
                yield (i, j, self.cost(solution, i, j))

    def best(self, solution):
        gen = self.generator(solution)
        best_from_pos, best_to_pos, min_cost = next(gen)
        for from_pos, to_pos, delta_cost in gen:
            if delta_cost < min_cost:
                min_cost = delta_cost
                best_from_pos = from_pos
                best_to_pos = to_pos
        return best_from_pos, best_to_pos, min_cost

    def first(self, solution):
        # gen = self.random_generator(solution)
        gen = self.generator(solution)
        best_from_pos, best_to_pos, min_cost = next(gen)
        if min_cost < 0:
            return best_from_pos, best_to_pos, min_cost
        for from_pos, to_pos, delta_cost in gen:
            if delta_cost < 0:
                return from_pos, to_pos, delta_cost
            if delta_cost < min_cost:
                min_cost = delta_cost
                best_from_pos = from_pos
                best_to_pos = to_pos
        return best_from_pos, best_to_pos, min_cost

    def move(self, solution, from_pos, to_pos, delta_cost=0):
        if to_pos < from_pos:
            solution.insert(to_pos, solution[from_pos])
            solution.pop(from_pos + 1)
        else:
            solution.insert(to_pos + 1, solution[from_pos])
            solution.pop(from_pos)
        return delta_cost


class MoveRevert(TSPmove):
    def cost(self, solution, start, end):
        if start == 0 and end == self.data.n - 1:
            return 0
        delta_costs = \
            - self._get_arc_cost_in_solution(solution, start - 1, start) \
            + self._get_arc_cost_in_solution(solution, start - 1, end) \
            - self._get_arc_cost_in_solution(solution, end, end + 1) \
            + self._get_arc_cost_in_solution(solution, start, end + 1)
        return delta_costs

    def random(self, solution):
        i = random.randint(0, self.data.n - 1)
        j = random.randint(0, self.data.n - 1)
        if i > j:
            i, j = j, i
        elif i == j:
            j = (j + 2) % (self.data.n - 1)
            if i > j:
                i, j = j, i

        # if i == 0:
        #     j = random.randint(i + 1, self.data.n - 2)
        # else:
        #     j = random.randint(i + 1, self.data.n - 1)
        return (i, j, self.cost(solution, i, j))

    def generator(self, solution):
        for i in range(self.data.n):
            if i == 0:
                end = self.data.n - 1
            else:
                end = self.data.n
            for j in range(i + 1, end):
                yield (i, j, self.cost(solution, i, j))

    def random_generator(self, solution):
        i_list = list(range(self.data.n))
        random.shuffle(i_list)
        for i in i_list:
            if i == 0:
                j_list = list(range(i + 1, self.data.n - 1))
                random.shuffle(j_list)
            else:
                j_list = list(range(i + 1, self.data.n))
                random.shuffle(j_list)
            for j in j_list:
                yield (i, j, self.cost(solution, i, j))

    def best(self, solution):
        gen = self.generator(solution)
        best_start, best_end, min_cost = next(gen)
        for start, end, delta_cost in gen:
            if delta_cost < min_cost:
                min_cost = delta_cost
                best_start = start
                best_end = end
        return best_start, best_end, min_cost

    def first(self, solution):
        # gen = self.random_generator(solution)
        gen = self.generator(solution)
        best_start, best_end, min_cost = next(gen)
        if min_cost < 0:
            return best_start, best_end, min_cost
        for start, end, delta_cost in gen:
            if delta_cost < 0:
                return start, end, delta_cost
            if delta_cost < min_cost:
                min_cost = delta_cost
                best_start = start
                best_end = end
        return best_start, best_end, min_cost

    def move(self, solution, start, end, delta_cost=0):
        for i in range((end - start + 1) // 2):
            solution[start + i], solution[end - i] = solution[end - i], solution[start + i],
        return delta_cost
