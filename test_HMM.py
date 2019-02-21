# Andrew Boghossian
# 2/17/19
from HMM import HMM
from Maze import Maze
from random import choice, random


# function to assign colors to floor spaces in a maze
def gen_random_colors(maze):
    possible_colors = ['r', 'g', 'b', 'y']  # color options
    maze_colors = {}  # dictionary mapping colors to floor spaces

    # loop through assigning random colors to floor spaces
    for x in range(maze.width):
        for y in range(maze.height):
            if maze.is_floor(x, y):
                maze_colors[(x, y)] = choice(possible_colors)
    return maze_colors


# function to move the robot in the maze and simulate the sensor
# for testing the HMM against ground truth
def move_robot(maze, maze_colors, new_location):
    possible_colors = ['r', 'g', 'b', 'y']  # color options

    # change location of robot in the maze
    maze.robotloc[0] = new_location[0]
    maze.robotloc[1] = new_location[1]

    actual_color = maze_colors[new_location]  # actual color of the square
    other_colors = [x for x in possible_colors if x != actual_color] # others

    # simulates sensor, 0.88 chance of corrrect color, 0.04 of others
    if random() < 0.88:
        sensor = actual_color
    elif random() < 0.92:
        sensor = other_colors[0]
    elif random() < 0.96:
        sensor = other_colors[1]
    elif random() <= 1:
        sensor = other_colors[2]

    return maze, actual_color, sensor


# function to test the HMM on a robot path, simulating the sensor
def test_HMM(maze, maze_colors, path):

    # lists tracking progression through the maze
    locations = [maze]
    actuals = '0'  # no color at first timestep
    sensors = '0'  # no sensor at first timestep

    # for resetting maze
    robot_startx = maze.robotloc[0]
    robot_starty = maze.robotloc[1]

    # loop through path updating tracking
    for loc in path:
        maze, actual_color, sensor_color = move_robot(maze, maze_colors, loc)
        locations.append(str(maze))
        actuals += actual_color
        sensors += sensor_color

    # reset
    maze.robotloc[0] = robot_startx
    maze.robotloc[1] = robot_starty

    # HMM to generate distributions based on sensor readings
    hmm = HMM(maze, sensors[1:], maze_colors)

    # generate path of distributions
    distribution_path = hmm.compute_distributions()  # filtering only
    smooth_path = hmm.compute_distrib_smoothing()  # forward-backward smoothing

    # prints out the actual maze, the readings and colors, and the distribution
    # at each timestep
    for timestep, distrib in enumerate(distribution_path):
        print('\ntime ' + str(timestep) + ' -----------')
        print('square color: ' + actuals[timestep])  # compare sensor and actual
        print('sensor color: ' + sensors[timestep])
        print('robot location:')
        print(locations[timestep])  # actual location (ground truth)
        print('distribution:')
        print(distrib)  # based on filtering
        print('\nsmoothed distribution:')
        print(smooth_path[timestep])  # based on forward-backward smoothing


# SOME TEST CODE:

# maze to test on
maze = Maze('test_maze.maz')

# dictionary of colors of floor spaces
maze_colors = gen_random_colors(maze)

# path taken by the robot
path = [(0, 0), (0, 1), (0, 2), (1, 2)]

test_HMM(maze, maze_colors, path)
