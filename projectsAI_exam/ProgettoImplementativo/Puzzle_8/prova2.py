import numpy as np
import heapq    
import copy

class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))
        
# Conta le tessere fuori posto
def h(state, goal):
    state = np.asarray(state).reshape(3, 3)
    goal = np.asarray(goal).reshape(3, 3)

    misplaced_tiles = np.sum(state != goal)  
    return misplaced_tiles


state=([[6, 2, 8],
        [4, 7, 1],
        [0, 3, 5]])

goal=([[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]])