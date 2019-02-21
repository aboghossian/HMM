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

        # transition model (constant 16x16 array)
        self.transition_model = self.compute_transition_model()

        # sensor models given color (constant 4x4 array)
        self.red_model = self.get_sensor_model('r')  # red
        self.blue_model = self.get_sensor_model('b')  # blue
        self.yellow_model = self.get_sensor_model('y')  # yellow
        self.green_model = self.get_sensor_model('g')  # green

    # computes a sequence of probability distributions given a sequence of
    # sensor readings (colors)
    def compute_distributions(self):
        # initialize
        state = self.start_state
        sequence = [np.flipud(state)]  # add start state to state sequence

        # loop through readings
        for color in self.sensor_readings:

            # implement transition model (reshape to 1x16 for multiplication)
            state = np.reshape(state, (1, 16))
            state = np.matmul(state, self.transition_model)

            # reshape back to 4x4
            state = np.reshape(state, (self.maze.width, self.maze.height))

            # implement sensor model based on color
            if color == 'r':
                state *= self.red_model
            if color == 'g':
                state *= self.green_model
            if color == 'b':
                state *= self.blue_model
            if color == 'y':
                state *= self.yellow_model

            # normalize and add flipped (to reflect maze orientation)
            state = self.normalize(state)
            sequence.append(np.flipud(state))

        return sequence

    # implements forward-backward algorithm to compute probability distribution
    def compute_distrib_smoothing(self):
        # both are initialized to uniform distributions
        forward_state = self.start_state
        backward_state = self.start_state

        # track the sequence starting at beginning and end
        forward_sequence = [np.flipud(forward_state)]
        backward_sequence = [np.flipud(backward_state)]

        # loop forward through readings
        for color in self.sensor_readings:

            # implement transition model (reshape to 1x16 for multiplication)
            forward_state = np.reshape(forward_state, (1, 16))
            forward_state = np.matmul(forward_state, self.transition_model)

            # reshape back to 4x4
            forward_state = np.reshape(forward_state, (self.maze.width, self.maze.height))

            # implement sensor model based on color
            if color == 'r':
                forward_state *= self.red_model
            if color == 'g':
                forward_state *= self.green_model
            if color == 'b':
                forward_state *= self.blue_model
            if color == 'y':
                forward_state *= self.yellow_model

            forward_state = self.normalize(forward_state)
            forward_sequence.append(np.flipud(forward_state))

        # loop backward through readings
        for color in self.sensor_readings[::-1]:

            # implement transition model (reshape to 1x16 for multiplication)
            backward_state = np.reshape(backward_state, (1, 16))
            backward_state = np.matmul(backward_state, self.transition_model)

            # reshape back to 4x4
            backward_state = np.reshape(backward_state, (self.maze.width, self.maze.height))

            # implement sensor model based on color
            if color == 'r':
                backward_state *= self.red_model
            if color == 'g':
                backward_state *= self.green_model
            if color == 'b':
                backward_state *= self.blue_model
            if color == 'y':
                backward_state *= self.yellow_model

            backward_state = self.normalize(backward_state)
            backward_sequence.append(np.flipud(backward_state))

        # reverse the backward sequence to reflect timestep
        backward_sequence.reverse()

        # combine forward and backward through multiplication
        smoothed = []
        for i, state in enumerate(forward_sequence):
            smooth = state * backward_sequence[i]  # multiply
            smooth = self.normalize(smooth)  # normalize
            smoothed.append(smooth)

        return smoothed

    # implements Viterbi algorithm to compute the most-likely path
    def compute_mlpath(self):
        pass

    # creates an array of probabilities (each location equal at start)
    # NOTE: the array a mirror of the maze when printing use np.flipud
    def get_start_state(self):
        start_state = np.zeros((self.maze.width, self.maze.height)) # empty

        for x in range(self.maze.width):
            for y in range(self.maze.height):

                if self.maze.is_floor(x, y):
                    start_state[y, x] = 1/len(self.maze_colors)

        return start_state

    # genrates a probability matrix for each square based on sensor model
    # sensor model:
    # if sensor reads a color then 0.88 chance the square is that color
    # 0.04 chance of other colors
    # divide all of these possibilities by number of each color
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

                    # otherwise probability = 0.12 it is not that color
                    # ****should this be broken down color by color?****
                    else:
                        num_color = self.num_colors[self.maze_colors[(x, y)]]
                        probability = 0.04/num_color
                        prob_matrix_sensor[y, x] = probability

        return prob_matrix_sensor

    # transition model:
    # generates a 16x16 matrix describing probability of moving from any square
    # to any other
    def compute_transition_model(self):

        # empty transition matrix
        trans_matrix = np.zeros((16, 16))

        # loop through the maze
        for y, column in enumerate(self.start_state):
            for x, value in enumerate(column):

                # convert to what value would be in a 1x16 array
                current = self.one_dimize((x, y))

                # get neighbors and track the total possible moves from square
                moves = self.get_moves((x, y))
                total_moves = len(moves)

                # for each move, incrememnt the probability in the matrix by
                # 1/total (probability of making that move from that square)
                for move in moves:
                    next = self.one_dimize(move)
                    trans_matrix[next, current] += 1/total_moves

        # transpose for multiplication
        return np.transpose(trans_matrix)

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

    # convert from two-dimensional location to one-dimensional location
    # for building transition model matrix
    def one_dimize(self, square):

        # y value x items in row + x value
        return self.maze.width * square[1] + square[0]

    # normalizes values of array
    def normalize(self, state):

        # sum
        total = np.sum(state)

        # divide each value by the sum
        state = state / total

        return state
