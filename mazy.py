# -*- coding: utf-8 -*-
"""
Maze creation and resolver class

Created on Sun Mar 20 18:24:35 2022

@author: Alex-932
@version: 0.7.1 (29/03/22)
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
        
        self.runner_path = {}

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
        self.start_distance = self.maze.get_values(self.start_point)[0]
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
        
    def get_orientation(self, position, prev_position, mode="Relative"):
        orientation = {}
        labels = ["West","North","East","South"]
        neighbors = maze.maze.get_neighbors(position, pattern="+")
        for k in range(len(neighbors)):
            orientation[neighbors[k]] = labels[k]
        if mode == "Relative":
            labels = ["Left","Forward","Right"]
            start_index = {"East":1, "North":2, "West":3,"South":0}
            rearranged_dir = [neighbors[k] for k in \
                              [2, 1, 0, 3, 2, 1, 0]]
            #E,N,W,S,E,N,W
            starter = start_index[orientation[prev_position]]
            orientation = {
                "Right": rearranged_dir[starter],
                "Forward": rearranged_dir[starter+1],
                "Left": rearranged_dir[starter+2]
                }
        return orientation
            
    def Joe(position, prev_position, neighbors):
        #Joe is a simple guy
        shuffle(neighbors)
        return neighbors.pop(), neighbors
    
    def Arthur(self, position, prev_position, neighbors):
        #Arthur always goes to the Right
        orientation_table = self.get_orientation(position, prev_position)
        ordered_directions = [orientation_table[k] \
                              for k in ["Right","Forward","Left"]\
                                  if orientation_table[k] in neighbors]
        return ordered_directions.pop(), ordered_directions
                
        
        
    def runner_choice(self, runner, position, prev_position, neighbors):
        if runner == "Joe":
            return Mazy.Joe(position, prev_position, neighbors)
        if runner == "Arthur":
            return self.Arthur(position, prev_position, neighbors)
        
    def path_shower(self, path, runner):
        value = 2
        for path in path :
            self.maze.set_values(path, value)
            value += 1
        self.maze.save(runner)
        self.maze.display("viridis")
        self.maze.grid = self.maze.saved["Original"]

    def maze_runner(self, runner="Joe"):
        position = self.start_point
        path = [[position]]
        explored = []
        crosspath = []
        prev_position = (0, 1)
        while position != self.exit_point:
            neighbors_raw = self.path_neighbors[position]
            neighbors = [k for k in neighbors_raw if k not in explored]
            neighbors_count = len(neighbors)
            explored.append(position)
            if neighbors_count == 0:
                #Dead end so back to the beginning of the path
                path[-1].append(position)
                prev_position, position = position, crosspath.pop()
                path.append([position])
            elif neighbors_count > 1:
                #Crosspath so the runner algorithm has to choose a direction
                choice, options = self.runner_choice(runner, position, \
                                                     prev_position, neighbors)
                path[-1].append(position)
                path.append([choice])
                crosspath += options
                prev_position, position = position, choice
            else :
                #We continue down the path
                path[-1].append(position)
                prev_position, position = position, neighbors[0]
        self.path_shower(path, runner)
        self.runner_path[runner] = {"Explored": explored, "Path": path,\
                                    "Distance": len(explored)}
        
if __name__ == "__main__":
    maze = Mazy(mode="fast")
    t = maze.maze_runner("Joe")
    t2 = maze.maze_runner("Arthur")