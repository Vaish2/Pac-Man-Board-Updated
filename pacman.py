"""
This module provides a function that navigates a 2-Dimensional board covered in coins which are picked up as you move over them, much like the game of PAC-MAN.
"""

from copy import deepcopy
import os

__author__ = "Vaishnavi Ganesan"


def convertBLtoTL(x, y, input2):
    # the x, y
    x, y = y, x
    return input2 - x, y


def convertTLtoBL(x, y, input2):
    x, y = y, x
    return x, input2 - y


def parseInput(input_file):    # parses the input from the .txt file and returns board_dimension, initial_position, movements, walls

    if not(os.path.exists(input_file)):  # checks if the path exists or not.
        print "Could not read file\File does not exist."
        return [-1, -1], [-1, -1], [-1, -1], [-1, -1]

    fileObject = open(input_file, "r")
    fileContent = fileObject.readlines()
    fileObject.close()
    noOfObstacles = len(fileContent) - 3

    board_dimension = [int(i) for i in fileContent[0].split()]  # dimension of the board, l x b
    initial_position = [int(i) for i in fileContent[1].split()]  # initial coordinates of the pacman
    movements = fileContent[2]
    walls = []
    for j in range(0, noOfObstacles):
        # converts the string into a list, and appends it to walls, which is a list of lists
        walls.append([int(i) for i in fileContent[j + 3].split()])
    if not(initial_position[0] >= 0 and initial_position[0] < board_dimension[0] and initial_position[1] >= 0 and initial_position[1] < board_dimension[1]):
        print "Invalid starting coordinates\n"
        return [-2, -1], [-1, -1], [-1, -1], [-1, -1] # Invalid O/P to denote invalid I/P
    return board_dimension, initial_position, movements, walls


class pacman_board:

    'Class for pacman game'

    def __init__(self, board_dimension, initial_position, walls):
        self.flag = 0   # 0 if the initial coordinates are valid, 1 if not
        self.coins = 0  # number of coins collected
        self.board_dimension = board_dimension  # dimension of the pacman Board
        self.current_position = initial_position  # the current position is initialised as the starting position
        self.walls = walls  # list of the walls
        self.path = []  # keeps track of all the coordinates that the pacman has been to
        if self.current_position in walls:
            print "The starting position cannot be a wall!\n"
            self.flag = 1   # Setting the flag to 1 to tell the parent function to return the invalid O/P
                            # to denote the invalid I/P
            return
        self.path.append(deepcopy(initial_position))  # adds the initial coordinate

    def print_current_pos(self):  # prints Current position. For debugging purposes
        print "Your current position is (%d,%d)" % (self.current_position[0], self.current_position[1])

    def print_coins(self):  # prints the number of coins collected. For debungging purposes
        print "You have collected %d coins" % self.coins

    def print_path(self):  # prints the path that the pacman has taken. For debugging purposes
        print "Your traced path is :"
        print self.path

    def go_one_step(self, direction):  # takes 'N' 'E' 'S' 'W' and updates the pacmans coordinates
        if(direction == 'N' or direction == 'S' or direction == 'E' or direction == 'W'):
            # Assume that the pacman goes to the next square, and check for its validity later.
            if(direction == 'N'):
                self.current_position[0] -= 1
            if(direction == 'S'):
                self.current_position[0] += 1
            if(direction == 'E'):
                self.current_position[1] += 1
            if(direction == 'W'):
                self.current_position[1] -= 1
            if((self.current_position[0] >= 0 and self.current_position[0] <= self.board_dimension[0] - 1) and ((self.current_position[1] >= 0 and self.current_position[1] <= self.board_dimension[1] - 1)) and (self.current_position not in self.walls)):
                # if the pacman has NOT crossed the edge of the board and not bumped into a wall
                if(self.current_position not in self.path):
                    self.coins += 1  # if the pacman has not been to this square already, then it has collected a coin
                self.path.append(deepcopy(self.current_position))  # append this square to the path of the pacman

            else:  # if the square is invalid, then reverse the changes to the current position
                if(direction == 'N'):
                    self.current_position[0] += 1
                if(direction == 'S'):
                    self.current_position[0] -= 1
                if(direction == 'E'):
                    self.current_position[1] -= 1
                if(direction == 'W'):
                    self.current_position[1] += 1
                return
        else:
            return


def pacman(input_file):
    board_dimension, initial_position, movements, walls = parseInput(input_file)
    if board_dimension == [-1, -1] or board_dimension == [-2, -1]:
        return [-1, -1], [-1, -1], 0

    # Converting the Bottom-right Coordinate system into the Top-Left Coordinate system
    initial_position = list(convertBLtoTL(initial_position[0], initial_position[1], board_dimension[1] - 1))
    while walls and not walls[-1]:
        walls.pop()
    for i in range(0, len(walls)):
        walls[i] = list(convertBLtoTL(walls[i][0], walls[i][1], board_dimension[1] - 1))
    board_dimension[0], board_dimension[1] = board_dimension[1], board_dimension[0]
    # End of conversion

    current_pac = pacman_board(board_dimension, initial_position, walls)
    if current_pac.flag == 1:
        return [-1, -1], [-1, -1], 0
    count = 0
    while(count < len(movements)):  # go through the list of directions
        current_pac.go_one_step(movements[count])
        count += 1

    # collect the final coordinates and the coins collected
    # and convert the top left coordinate system into bottom left
    board_dimension[0], board_dimension[1] = board_dimension[1], board_dimension[0]
    tempList = [current_pac.current_position[0], current_pac.current_position[1]]
    tempList = convertTLtoBL(tempList[0], tempList[1], board_dimension[1] - 1)
    final_pos_x = tempList[0]
    final_pos_y = tempList[1]

    coins_collected = current_pac.coins

    return final_pos_x, final_pos_y, coins_collected
