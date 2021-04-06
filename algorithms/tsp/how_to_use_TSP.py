from algorithms.tsp.TSPclass import TSP

"""How to start?"""
# 1. Use prepared dataset
# tsp = TSP('tsp/examples/30.csv')

# 2. Generate random n nodes
tsp = TSP(10)

# And you can write coords in csv file
# tsp.data.write_coords()

# 3. Set nodes
# tsp = TSP([(1, 2), (2, 2), (0.5, 0), (3, 3)])

"""How to solve?"""
# You can choice
# tsp.LSF.solve_info()
# tsp.LSB.solve_info()

tsp.algo.solve(40)
# print(tsp.algo.get_info())

print(tsp.algo.get_plot(2))
print(tsp.algo.solutions[2])
# print(tsp.algo.get)
print(tsp.algo.G.edges)

print(tsp.algo.get_plot(3))
print(tsp.algo.solutions[3])
print(tsp.algo.G.edges)
# tsp.algo.solve(40)
# print(tsp.algo.get_info())
"""How to animate?"""
# tsp.LSF.animation()
