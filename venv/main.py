import math
import random
import time
import sys
import csv
import copy
import logging
from puzzles import *


class Variable:
    def __init__(self, i):
        self.spaces = []
        self.index = i
        self.is_occupied = False
        self.weight = 0


class Puzzle:
    def __init__(self, table, words, vars, word_is_used):
        self.table = table
        self.words = words
        self.vars = vars
        self.word_is_used = word_is_used


class Word:
    def __init__(self):
        self.chars = []
        self.isUsed = False


def print_puzzle(Puzzle):
    for row in Puzzle.table:
        print (row)
        logging.info(row)
    logging.info('')


def print_vars(Puzzle):
    for x in Puzzle.vars:
        print(x.index, x.spaces)


def define_variables(table):
    vars = []
    vars_row = -1
    for row in range(len(table)):
        flag = False
        for col in range(len(table[row])):
            if table[row][col] == '_':
                if flag:
                    vars_row = vars_row + 1
                    vars.append(Variable(vars_row))
                    flag = False
                vars[vars_row].spaces.append([row, col])
            if table[row][col] == '#':
                flag = True
        # vars_row = vars_row + 1

    for col in range(len(table[0])):
        flag = False
        for row in range(len(table)):
            if table[row][col] == '_':
                if flag:
                    vars_row = vars_row + 1
                    vars.append(Variable(vars_row))
                    flag = False
                vars[vars_row].spaces.append([row, col])
            if table[row][col] == '#':
                flag = True
        # vars_row = vars_row + 1
    return vars


def next_variable(Puzzle):
    for var in Puzzle.vars:
        if len(var.spaces) == 1:
            continue
        if var.is_occupied == False:
            var.is_occupied = True
            return var.index
    return -1


def words_in_variable(Puzzle, var):  # returns the number of words that fit into variable
    count = 0
    for word in Puzzle.words:
        if len(var.spaces) != len(word):
            continue
        temp_puzzle = copy.deepcopy(Puzzle.table)
        word_fits = True
        for x in range(len(word)):
            row = var.spaces[x][0]
            col = var.spaces[x][1]
            if Puzzle.table[row][col] == '_' or Puzzle.table[row][col] == word[x]:
                temp_puzzle[row][col] = word[x]
            else:
                word_fits = False
        if word_fits:
            count = count + 1
    return count


def next_mrv_variable(Puzzle):
    max = len(Puzzle.words) + 1
    for var in Puzzle.vars:
        if len(var.spaces) == 1:
            var.weight = False
            continue
        if var.is_occupied == False:
            var.weight = words_in_variable(Puzzle, var)
            if var.weight < max:
                max = var.weight
                varptr = var
    try:  # check if varptr is unassigned, if not it means no variables left
        varptr
    except NameError:
        return -1
    varptr.is_occupied = True
    return varptr.index


def solve(Puzzle):
    global counter
    counter = counter + 1
    var_i = next_mrv_variable(Puzzle)

    if var_i == -1:
        return 1

    i = 0
    for word in Puzzle.words:
        if Puzzle.word_is_used[i] == True:
            i = i + 1
            continue
        prev_table = copy.deepcopy(Puzzle.table)
        if check_word(Puzzle, word, var_i):
            Puzzle.word_is_used[i] = True
            if solve(Puzzle):
                return 1
            else:
                Puzzle.table = copy.deepcopy(prev_table)
                Puzzle.word_is_used[i] = False
        i = i + 1
    Puzzle.vars[var_i].is_occupied = False
    return 0


def check_if_solved(Puzzle):
    for row in Puzzle.table:
        for elem in row:
            if elem == '_':
                return 0
    return 1


def check_word(Puzzle, word, var_i):  # Checks and inserts the word
    if len(Puzzle.vars[var_i].spaces) != len(word):
        return 0
    temp_puzzle = copy.deepcopy(Puzzle.table)
    word_fits = True
    for x in range(len(word)):
        row = Puzzle.vars[var_i].spaces[x][0]
        col = Puzzle.vars[var_i].spaces[x][1]
        if Puzzle.table[row][col] == '_' or Puzzle.table[row][col] == word[x]:
            temp_puzzle[row][col] = word[x]
        else:
            word_fits = False
    if word_fits:
        Puzzle.table = copy.deepcopy(temp_puzzle)
        print_puzzle(Puzzle)
        print(' ')
        return 1
    else:
        return 0


words = words3
table = puzzle3
word_is_used = [False] * len(words)
vars = define_variables(table)

logging.basicConfig(filename="logfilename.log", level=logging.INFO)
Puzzle = Puzzle(table, words, vars, word_is_used)
print_puzzle(Puzzle)
print(Puzzle.words)
print_vars(Puzzle)

start_time = time.time()
counter = 0
if solve(Puzzle):
    print("YAY! SOLVED!\n")
    print("It took", time.time() - start_time, "seconds to solve this puzzle.")
    print(counter, "backtrack calls")
    print_puzzle(Puzzle)
else:
    print("SOLUTION NOT FOUND!\n")
    print_puzzle(Puzzle)
