# -*- coding: utf-8 -*-
"""
Maze creation

Created on Sun Mar 20 18:24:35 2022

@author: Alex-932
@version: 0.7 (20/03/22)
"""

import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
from random import shuffle
import time

Y, X, Tor = 21, 31, False
drilled = []
path_neighbors = {}

def parameters():
    global Y, X, Tor
    Y = int(input("Y dimension (uneven only) : "))
    X = int(input("X dimension (uneven only) : "))
    Tor = bool(int(input("Is the maze toroidal ? (1 or 0) ")))

start_point = (1, 1)
exit_point = (X-2, Y-2)

maze = Grid(X, Y, tor=Tor, value=0)

def starter():
    maze.set_values([start_point], 2)
    maze.set_values([exit_point], 3)

def driller(position, middle_point, next_point):
    global exit_point
    if next_point != exit_point :
        coord_list = [next_point, middle_point]
    else :
        coord_list = [middle_point]
    maze.set_values(coord_list, 1)
    

def worker():
    global start_point, drilled
    primers = [start_point]
    drilled = [start_point]
    while len(primers) != 0:
        shuffle(primers)
        (px, py) = primers.pop()
        options = [(x, y) for (x, y) in \
                   [(px-2, py), (px, py+2), (px+2, py), (px, py-2)] \
                       if x in range(maze._x) \
                           and y in range(maze._y) \
                               and (x, y) not in drilled]
        shuffle(options)
        if len(options) >= 1 :
            next_p = options.pop()
            mid_p = (int(px+(next_p[0]-px)/2), int(py+(next_p[1]-py)/2))
            driller((px, py), mid_p, next_p)
            drilled.append(next_p)
            drilled.append(mid_p)
            primers += [(px, py), next_p]
            
    for coord in maze.coord :
        print(coord)
        if maze.get_values(coord)[0] == 1 and coord not in drilled:
            drilled.append(coord)
            
    maze.save("Original")
            
def compute_path_neighbors():
    global drilled, path_neighbors
    for k in drilled:
        neighbors = [coord for coord in maze.get_neighbors(k, pattern="+")\
                     if coord in drilled]
        path_neighbors[k] = neighbors
    
def colored_map():
    global exit_point, path_neighbors, drilled, start_point
    colored = [exit_point]
    primers = colored.copy()
    while len(drilled) != len(colored) :
        position = primers.pop()
        neighbors = [coord for coord in path_neighbors[position] \
                     if coord not in colored]
        maze.set_values(neighbors, maze.get_values(position)[0]+1)
        primers += neighbors
        colored += neighbors
    maze.save("distance")
    start_distance = maze.get_values(start_point)
    maze.set_values([exit_point, start_point], \
                    max(maze.get_values(maze.coord))+10)
    maze.grid = maze.saved[0]
    return 

def maze_quality():
    pass

def maze_builder():
    start_time = time.time()    
    starter()
    #plt.imshow(maze.grid, cmap="bone")
    worker()
    compute_path_neighbors()
    print("Build time : ", time.time()-start_time, "s")
    maze.display() 

maze_builder()      
            
        
    
    
    
    

def maze_runner():
    global start_point
    explored_cells = [start_point]
    position = start_point
    while False == True:
        pass
    return True        
