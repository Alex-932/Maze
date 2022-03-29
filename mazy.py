# -*- coding: utf-8 -*-
"""
Maze creation

Created on Sun Mar 20 18:24:35 2022

@author: Alex-932
@version: 0.7 (20/03/22)
"""

from grid import Grid
from random import shuffle
import time


class Mazy() :

    def __init__(self, mode="config"):
        
        if mode == "fast":
            self._y = 21
            self._x = 31
            self._tor = False
            self.start_point = (1, 1)
            self.exit_point = (self._x-2, self._y-2)
            self.maze = Grid(self._x, self._y, tor=self._tor, value=0)
            
        elif mode == "config":
            self._y = int(input("Y dimension (uneven only) : "))
            self._x = int(input("X dimension (uneven only) : "))
            self._tor = bool(int(input("Is the maze toroidal ? (1 or 0) ")))
            
        self.drilled = []
        self.path_neighbors = {}

        self.maze.set_values([self.start_point], 2)
        self.maze.set_values([self.exit_point], 3)
        
        self.maze_builder()

    def driller(self, position, middle_point, next_point):
        if next_point != self.exit_point :
            coord_list = [next_point, middle_point]
        else :
            coord_list = [middle_point]
        self.maze.set_values(coord_list, 1)
    

    def worker(self):
        primers = [self.start_point]
        self.drilled = [self.start_point]
        while len(primers) != 0:
            shuffle(primers)
            (px, py) = primers.pop()
            options = [(x, y) for (x, y) in \
                       [(px-2, py), (px, py+2), (px+2, py), (px, py-2)] \
                           if x in range(self._x) \
                               and y in range(self._y) \
                                   and (x, y) not in self.drilled]
            shuffle(options)
            if len(options) >= 1 :
                next_p = options.pop()
                mid_p = (int(px+(next_p[0]-px)/2), int(py+(next_p[1]-py)/2))
                self.driller((px, py), mid_p, next_p)
                self.drilled.append(next_p)
                self.drilled.append(mid_p)
                primers += [(px, py), next_p]
                
        for coord in self.maze.coord :
            if self.maze.get_values(coord)[0] == 1 \
                and coord not in self.drilled:
                self.drilled.append(coord)
                
        self.maze.save(name="Original")
            
    def compute_path_neighbors(self):
        for k in self.drilled:
            neighbors = [coord for coord in \
                         self.maze.get_neighbors(k, pattern="+")\
                         if coord in self.drilled]
            self.path_neighbors[k] = neighbors
    
    def colored_map(self):
        colored = [self.exit_point]
        primers = colored.copy()
        while len(self.drilled) != len(colored) :
            position = primers.pop()
            neighbors = [coord for coord in self.path_neighbors[position] \
                         if coord not in colored]
            self.maze.set_values(neighbors, \
                                 self.maze.get_values(position)[0]+1)
            primers += neighbors
            colored += neighbors
        self.maze.save(name="Distance")
        self.start_distance = self.maze.get_values(self.start_point)
        self.maze.set_values([self.exit_point, self.start_point], \
                        max(self.maze.get_values(self.maze.coord))+10)
        self.maze.grid = self.maze.saved["Original"]

    def maze_builder(self):
        start_time = time.time()    
        self.worker()
        self.compute_path_neighbors()
        print("Build time : ", time.time()-start_time, "s")
        self.maze.display()
        self.colored_map()
        
if __name__ == "__main__":
    maze = Mazy(mode="fast")