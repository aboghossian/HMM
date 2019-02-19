# Andrew Boghossian
# 2/17/19
from HMM import HMM
from Maze import Maze
import numpy as np

# maze to test on
maze = Maze('test_maze.maz')

# string of sensor readings (colors r, b, g, y)
reading_string = 'rbgyybr'

# dictionary of colors of floor spaces
# currently set up so each column is the same color
maze_colors = {(0, 0): 'r',
               (0, 1): 'r',
               (2, 1): 'y',
               (3, 1): 'g',
               (0, 2): 'r',
               (1, 2): 'b',
               (2, 2): 'y',
               (3, 2): 'g',
               (1, 3): 'b',
               (3, 3): 'g'}

# HMM problem based on the maze and color map
hmm = HMM(maze, reading_string, maze_colors)
distribution_path = hmm.compute_distributions()
for timestep, distrib in enumerate(distribution_path):
    print('time ' + str(timestep) + ':')
    print(distrib)
