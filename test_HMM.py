# Andrew Boghossian
# 2/17/19
from HMM import HMM
from Maze import Maze
from random import choice


# function to assign colors to floor spaces in a maze
def gen_random_colors(maze):
    possible_colors = ['r', 'g', 'b', 'y']  # color options
    maze_colors = {}  # dictionary mapping colors to floor spaces

    # loop through assigning random colors to floor spaces
    for x in range(self.maze.width):
        for y in range(self.maze.height):
            if self.maze.is_floor(x, y):
                maze_colors[(x, y)] = choice(possible_colors)
    return maze_colors


# maze to test on
maze = Maze('test_maze.maz')

# string of sensor readings (colors r, b, g, y)
reading_string = 'bbyyggr'

# dictionary of colors of floor spaces
# currently set up so each column is the same color in test_maze.maz
# if using other mazes use gen_random_colors(maze) to make this dictionary
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
