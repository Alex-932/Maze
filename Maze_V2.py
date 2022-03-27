# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 18:24:35 2022

@author: Alex-932
@version: 1.0 (20/03/22)
"""

import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
from random import randint, shuffle

Y, X, Tor = 21, 31, 0

def parameters():
    global Y, X, Tor
    Y = int(input("Y dimension (uneven only) : "))
    X = int(input("X dimension (uneven only) : "))
    Tor = bool(int(input("Is the maze toroidal ? (1 or 0) ")))

start_point = (1, 1)
exit_point = (X-2, Y-2)

maze = Grid(X, Y, tor=Tor, value=1)

# walls are cells that stay at a value of 1.
walls = [(i, j) for (i, j) in maze.coord if (i%2)+(j%2) == 0]

# lanes are cells where the player can walk and does not have a value of 1.
lanes = [(i, j) for (i, j) in maze.coord if (i, j) not in walls]

# lanes_neighbors is a dictionnary that save the nighboring cells coordinates
# for each lane cells.
lanes_neighbors = {}
maze.compute_neighbors()
for (i, j) in lanes :
    raw_neighbors = maze.neighbors[str((i, j))]
    neighbors = [k for k in raw_neighbors if k not in walls]
    lanes_neighbors[(i, j)] = neighbors
    
# lanes_next_cell = {}
# for (i, j) in lanes :
#     raw_next_cell = [(i-2, j), (i, j+2), (i+2, j), (i, j-2)]
#     if i == 1 :
#         lanes_next_cell[(i, j)] = raw_next_cell[1:]
#     elif j == 1 :
#         lanes_next_cell[(i, j)] = raw_next_cell[:3]
#     elif j*i == 1 :
#         lanes_next_cell[(i, j)] = raw_next_cell[:3]
# doors are cells that can switch between being a wall or a lane.
doors = [(i, j) for (i, j) in lanes if (i%2)+(j%2) == 1 and i not in [0, X-1]\
         and j not in [0, Y-1]]

if not Tor :
    # borders are the cells that are the limit of the grid if the grid is non toroidal
    borders = [(i, j) for (i, j) in maze.coord if i in [0,X-1] or j in [0,Y-1]]
    walls += borders

def starter():
    maze.set_value([start_point], 2)
    maze.set_value([exit_point], 3)
    if Tor :
        maze.set_value(borders, 0)
        maze.set_value(walls, 1)

def driller(position, next_point):
    global exit_point
    (px, py), (fx, fy) = position, next_point
    middle_point = (int(px+(fx-px)/2), int(py+(fy-py)/2))
    if next_point != exit_point :
        coord_list = [next_point, middle_point]
    else :
        coord_list = [middle_point]
    print("List drill : ", coord_list)
    maze.set_value(coord_list, 0)
    

def builder():
    global start_point
    primers = [start_point]
    drilled = [start_point]
    time = 0
    while len(primers) != 0:
        shuffle(primers)
        (px, py) = primers.pop()
        options = [(x, y) for (x, y) in \
                   [(px-2, py), (px, py+2), (px+2, py), (px, py-2)] \
                       if x in range(maze.grid.shape[1]) \
                           and y in range(maze.grid.shape[0]) \
                               and (x, y) not in drilled]
        print("Options : ", options)
        shuffle(options)
        if len(options) >= 1 :
            next_position = options.pop()
            driller(position=(px, py), next_point=next_position)
            drilled.append(next_position)
            primers += [(px, py), next_position]
            print("Primers : ", primers)
        
        time += 1
            
        
        
            
            
                
            
    
    
    
starter()
plt.imshow(maze.grid, cmap="bone")
builder()
plt.imshow(maze.grid, cmap="bone")
