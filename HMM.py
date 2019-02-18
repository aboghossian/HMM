# Andrew Boghossian
# 2/17/19

import numpy as np


class HMM:

    def __init__(self, maze, sensor_readings, maze_colors):

        self.maze = maze  # maze that the robot is in
        self.sensor_readings = sensor_readings  # sensor readings from the robot
        self.maze_colors = maze_colors  # colors of each square of the maze
        self.start_state = np.zeros((maze.width, maze.height)) # placeholder

        # builds a dictionary tracking how many of each color in the maze
        # for generating the probability of being in a square based on color
        self.num_colors = {'r': 0,
                           'b': 0,
                           'g': 0,
                           'y': 0}
        for value in self.maze_colors.values():
            self.num_colors[value] += 1

        # creates an array of probabilities (each location equal at start)
        # NOTE: the array a mirror of the maze when printing use np.flipud
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    self.start_state[y, x] = 1/len(maze_colors)

    # genrates a probability matrix for each square based on sensor model
    def get_sensor_model(self, state, color):
        # sensor model:
        # if sensor reads a color then 0.88 chance the square is that colors
        # 0.04 chance of other color
        # divide all of these possibilities by number of each square of a color
        prob_matrix_sensor = np.ones((self.maze.width, self.maze.height))

        for x in range(self.maze.width):
            for y in range(self.maze.height):

                # probability is probability it is that color/#color in maze
                if maze_colors[(x, y)] == color:
                    probability = 0.88/self.num_colors[color]
                    prob_matrix_sensor[y, x] *= probability
                else:
                    probability = 0.04/self.num_colors[maze_colors[(x, y)]]
                    prob_matrix_sensor[y, x] *= probability

    # transition model:
    # assuming a uniform probability of choosing any move, the chance of
    # moving to a given square is the number of ways to move to that square
    # stays constant for the entire problem
    def compute_transition_model(self):
        pass

    def compute_distribution(self, reading, state):
        pass

    # returns a list of legal moves from a given square (tuple)
    def get_moves(self, square):
        pass
