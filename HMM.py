# Andrew Boghossian
# 2/17/19
import numpy as np


# class that uses a Hidden Markov Model to solve a Mazeworld problem
class HMM:

    def __init__(self, maze, sensor_readings, maze_colors):

        self.maze = maze  # maze that the robot is in
        self.sensor_readings = sensor_readings  # sensor readings from the robot
        self.maze_colors = maze_colors  # colors of each square of the maze
        self.start_state = self.get_start_state() # genrate initial distribution

        # builds a dictionary tracking how many of each color in the maze
        # for generating the probability of being in a square based on color
        self.num_colors = {'r': 0,
                           'b': 0,
                           'g': 0,
                           'y': 0}
        for color in self.maze_colors.values():
            self.num_colors[color] += 1  # increment number of that color

        # transition model (constant)
        self.transition_model = self.compute_transition_model()

        # sensor models given color (constant)
        self.red_model = self.get_sensor_model('r')  # red
        self.blue_model = self.get_sensor_model('b')  # blue
        self.yellow_model = self.get_sensor_model('y')  # yellow
        self.green_model = self.get_sensor_model('g')  # green
        print(self.transition_model)
        print('RED--------------')
        print(self.red_model)
        print('BLUE-------------')
        print(self.blue_model)
        print('GREEN------------')
        print(self.green_model)
        print('YELLOW-----------')
        print(self.yellow_model)

    # creates an array of probabilities (each location equal at start)
    # NOTE: the array a mirror of the maze when printing use np.flipud
    def get_start_state(self):
        start_state = np.zeros((self.maze.width, self.maze.height)) # empty

        for x in range(self.maze.width):
            for y in range(self.maze.height):

                if self.maze.is_floor(x, y):
                    start_state[y, x] = 1/len(self.maze_colors)

    # genrates a probability matrix for each square based on sensor model
    # sensor model:
    # if sensor reads a color then 0.88 chance the square is that color
    # 0.04 chance of other colors
    # divide all of these possibilities by number of each square of a color
    def get_sensor_model(self, color):

        # placeholder, values will be updated
        prob_matrix_sensor = np.zeros((self.maze.width, self.maze.height))

        # loop through maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):

                if self.maze.is_floor(x, y):

                    # probability is probability it is that color/#color in maze
                    # if matches sensor probability = 0.88 it is that color
                    if self.maze_colors[(x, y)] == color:
                        probability = 0.88/self.num_colors[color]
                        prob_matrix_sensor[y, x] = probability

                    # otherwise probability = 0.04 it is one of the three others
                    else:
                        probability = 0.04/self.num_colors[self.maze_colors[(x, y)]]
                        prob_matrix_sensor[y, x] = probability

        return prob_matrix_sensor

    # transition model:
    # assuming a uniform probability of choosing any move, the chance of
    # moving to a given square is the number of ways to move to that square
    # stays constant for the entire problem
    def compute_transition_model(self):
        moves_to = {}  # tracks number of moves to a given square
        total_moves = 0  # tracks the total number of possible moves

        # loop through possible locations
        for square in self.maze_colors:

            # generate neighbors of those locations
            neighbors = self.get_moves(square)
            for neighbor in neighbors:

                # add to dictionary or increment value if already in
                if neighbor in moves_to:
                    moves_to[neighbor] += 1
                else:
                    moves_to[neighbor] = 1
                total_moves += 1  # increment total moves

        # placeholder, values will be updated
        prob_matrix_transition = np.zeros((self.maze.width, self.maze.height))

        # for each square probability of moving to it is number of moves to it
        # divided by total possible moves (assumes moves are random)
        for square in moves_to:
            probability = moves_to[square]/total_moves
            x, y = square
            prob_matrix_transition[y, x] = probability

        return prob_matrix_transition


    def compute_distribution(self, reading, state):
        pass

    # returns a list of legal moves from a given square (tuple)
    def get_moves(self, square):
        neighbors = []  # empty list of neighbors of a square

        # loop through change values
        for change in [-1, 1, -1, 1]:

            # first 2 neighbors will be x change
            if len(neighbors) < 2:
                neighbor = (square[0] + change, square[1])

            # last 2 will be y change
            else:
                neighbor = (square[0], square[1] + change)

            # ensure they are within the maze, if it is add it
            if self.maze.is_floor(neighbor[0], neighbor[1]):
                neighbors.append(neighbor)  # add to list
            # otherwise the move stays at the original square
            else:
                neighbors.append(tuple(square))

        return neighbors
