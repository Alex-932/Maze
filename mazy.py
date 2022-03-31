# -*- coding: utf-8 -*-
"""
Maze creation and resolver class

Created on Sun Mar 20 18:24:35 2022

@author: Alex-932
@version: 0.7.4
"""

from grid import grid
from random import shuffle
from math import sqrt
import time

class mazy():

    def __init__(self, mode="config"):
        """
        The mazy class provide algorithms to create and resolve a maze.

        Parameters
        ----------
        mode : str, optional
            Intended for benchmarking. The default is "config".
            The other option is "fast" which set the variables.

        Returns
        -------
        None.

        """
        
        if mode == "fast":
            self._y = 21
            self._x = 31
            self._tor = False
            self.start_point = (1, 1)
            self.exit_point = (self._x-2, self._y-2)
            self.maze = grid(self._x, self._y, tor=self._tor, value=0)
            
        elif mode == "config":
            self._y = int(input("Y dimension (uneven only) : "))
            self._x = int(input("X dimension (uneven only) : "))
            self._tor = bool(int(input("Is the maze toroidal ? (1 or 0) ")))
            self.start_point = (1, 1)
            self.exit_point = (self._x-2, self._y-2)
            self.maze = grid(self._x, self._y, tor=self._tor, value=0)
            
        self.drilled = []
        self.path_neighbors = {}

        self.maze.set_values([self.start_point], 2)
        self.maze.set_values([self.exit_point], 3)
        
        self.maze_builder()
        
        self.runner_path = {}

    def driller(self, position, middle_point, next_point):
        """
        Set the values of the given cells to 1 which is the value of a 
        "path" cell.

        Parameters
        ----------
        position : tuple
            Coordinates of the current position of the runner.
        middle_point : tuple
            Coordinates of the next cell on the path the runner is 
            going to take.
        next_point : tuple
            Coordinates of the cell where the runner will 
            make a break before the next move.

        Returns
        -------
        None.

        """
        if next_point != self.exit_point :
            coord_list = [next_point, middle_point]
        else :
            coord_list = [middle_point]
        self.maze.set_values(coord_list, 1)
    

    def worker(self):
        """
        Worker is the algorithm that create the maze.

        Returns
        -------
        None.

        """
        primers = [self.start_point]
        #List that save the coordinates of the paths that the worker can take.
        #For example, at each cell, the worker can go one direction and the 
        #others are added to that list to come back at them later.  
        self.drilled = [self.start_point]
        #List that save the cell that are now "path".
        while len(primers) != 0:
            shuffle(primers)
            (px, py) = primers.pop()
            #A random primer or starter is chosen.
            options = [(x, y) for (x, y) in \
                       [(px-2, py), (px, py+2), (px+2, py), (px, py-2)] \
                           if x in range(self._x) \
                               and y in range(self._y) \
                                   and (x, y) not in self.drilled]
            #That list contains the neighboring cells coordinates that the
            #worker can drill.
            shuffle(options)
            if len(options) >= 1 :
                #We make sure there are options available for our worker.
                #Else it's a dead end so we lookback to choose another primer.
                next_p = options.pop()
                #Worker destination.
                mid_p = (int(px+(next_p[0]-px)/2), int(py+(next_p[1]-py)/2))
                #Coordinates between the current position and the destination.
                self.driller((px, py), mid_p, next_p)
                #We drill the cells. 
                self.drilled.append(next_p)
                self.drilled.append(mid_p)
                #The drilled cells are added to the "drilled" list.
                primers += [(px, py), next_p]
                #We add the coordinates of the cell that the 
                #worker could continue from.
        #We finally add all drilled cell to "drilled".
        for coord in self.maze.coord :
            if self.maze.get_values(coord)[0] == 1 \
                and coord not in self.drilled:
                self.drilled.append(coord)
        #We save the maze in order to use it later.        
        self.maze.save(name="Original")
            
    def compute_path_neighbors(self):
        """
        Method to generate a dictionnary (self.path_neighbors) containing, 
        for each path cell, all neighboring cells that are also path cell. 
        Used to speed up process.

        Returns
        -------
        None.

        """
        for k in self.drilled:
            neighbors = [coord for coord in \
                         self.maze.get_neighbors(k, pattern="+")\
                         if coord in self.drilled]
            self.path_neighbors[k] = neighbors
            #keys are the coordinates (x, y) and values are a list of tuple.
    
    def maze_coloration(self):
        """
        Method to color the maze. The color scale represent the distance to
        the exit point. The brighter the color is, the farthest the cell is.
        The colored maze is saved as "Distance" in self.maze.saved.
        
        Returns
        -------
        None.

        """
        colored = [self.exit_point]
        #Colored is a list which save the cell that are already colored.
        primers = colored.copy()
        #Primers as the same function as in the worker method.
        while len(self.drilled) != len(colored) :
            #The coloration continue as long as all drilled (or path) cell 
            #aren't colored.
            position = primers.pop()
            neighbors = [coord for coord in self.path_neighbors[position] \
                         if coord not in colored]
            #Neighbors stores the neighboring cells that are not colored.
            self.maze.set_values(neighbors, \
                                 self.maze.get_values(position)[0]+1)
            #The value of those neighbors cell is set as the value of the 
            #current cell + 1.
            primers += neighbors
            colored += neighbors
            #Neighbors are added to the primers list to continue 
            #the coloration to their neighbors and so on. They're also added
            #to the colored list in order not to reprocess them.
        self.maze.save(name="Distance")
        #The colored maze is saved as "Distance" in self.maze.saved.
        self.start_distance = int(self.maze.get_values(self.start_point)[0])
        #The value of the start_point is saved as it is a quality index.
        self.maze.set_values([self.exit_point, self.start_point], \
                        max(self.maze.get_values(self.maze.coord))+10)
        #The cell value of start_point and exit_point are replaced with the 
        #maximum value of the maze's cells +10 to better see them in the graph.
        self.maze.grid = self.maze.saved["Original"]
        #The maze grid is set back to the clean and original maze in order to 
        #continue working with it.

    def maze_builder(self):
        """
        Method that create the maze and execute some methods that will be
        needed in order to solve the maze. 

        Returns
        -------
        None.

        """
        start_time = time.time()    
        self.worker()
        self.compute_path_neighbors()
        print("Build time : ", time.time()-start_time, "s")
        self.maze.display()
        self.maze_coloration()
        
    def get_orientation(self, position, prev_position, mode="Relative"):
        """
        Method used to resolve the maze. It compute the directions of
        the neighboring cell of the given position.

        Parameters
        ----------
        position : tuple
            Coordinates of the current cell the runner is on.
        prev_position : tuple
            Previous position of the runner.
        mode : str, optional
            How the direction are returned. The default is "Relative".
            "Relative" : direction relative to the runner (Right, Left, ...)
            "Absolute" : direction relative the maze (North, East, ...)

        Returns
        -------
        orientation : dict
            Keys are the coordinates of the neighboring cell (tuple). 
            Values are the direction for the neighbor cell (str).

        """
        orientation = {}
        labels = ["West","North","East","South"]
        #Labels are the absolute direction given by the grid.get_neighbors()
        #method.
        neighbors = self.maze.get_neighbors(position, pattern="+")
        #Neighbors of the current position cell are reprocessed and retrieved.
        for k in range(len(neighbors)):
            orientation[neighbors[k]] = labels[k]
            #Each cell coordinates gets its absolute orientation.
        if mode == "Relative":
            labels = ["Left","Forward","Right"]
            #There's only 3 directions as backward is useless
            start_index = {"East":1, "North":2, "West":3,"South":0}
            #grid.get_neighbors() return neighboring cells in the specific 
            #order : West, North, East, South.
            #rearranged_dir contains the coordinates of the cell in a specific
            #order allow us to compute faster : E,N,W,S,E,N,W.
            rearranged_dir = [neighbors[k] for k in \
                              [2, 1, 0, 3, 2, 1, 0]]
            #Each time, we get the direction of the previous cell the runner 
            #was. The 3 previous coordinates in rearranged_dir are exactly in
            #that specific order : Right, Forward, Left.
            starter = start_index[orientation[prev_position]]
            #starter is the index from where to begin in rearranged_dir to get
            #the right coordinates.
            orientation = {
                rearranged_dir[starter]: "Right",
                rearranged_dir[starter+1]: "Forward",
                rearranged_dir[starter+2]: "Left"
                }
        return orientation
            
    def ICR(position, neighbors):
        """
        ICR is a simple guy, he choose a path randomly.
        ICR stands for I Choose Randomly.

        Parameters
        ----------
        position : tuple
            Coordinates of the current cell the runner is on.
        prev_position : tuple
            Previous position of the runner.
        neighbors : list of tuple
            Coordinates of the neighboring cells from the current position.

        Returns
        -------
        tuple
            Coordinates of the first cell of the path the runner will take.
        list of tuple
            Coordinates of the other paths the runner could take later.

        """
        shuffle(neighbors)
        return neighbors.pop(), neighbors
    
    def IGR(self, position, prev_position, neighbors):
        """
        IGR always choose the rightmostpath. So the directions in that 
        order : Right, Forward, Left.
        IGR stands for I Go Right.

        Parameters
        ----------
        position : tuple
            Coordinates of the current cell the runner is on.
        prev_position : tuple
            Previous position of the runner.
        neighbors : list of tuple
            Coordinates of the neighboring cells from the current position.

        Returns
        -------
        tuple
            Coordinates of the first cell of the path the runner will take.
        list of tuple
            Coordinates of the other paths the runner could take later.

        """
        orientation_table = self.get_orientation(position, prev_position)
        ordered_directions = [k for k in orientation_table \
                                  if k in neighbors]
        #We just make sure that the directions provided by the 
        #mazy.get_orientation are actual paths.
        ordered_directions.reverse()
        #That list is reversed so the directions are "Left" then "Forward".
        #Important because later, in the case of a deadend, the last value of 
        #the intesrection list will be taken which would be "Left" if not 
        #reversed.
        return ordered_directions.pop(0), ordered_directions
    
    def IGL(self, position, prev_position, neighbors):
        """
        IGL always choose the leftmostpath. So the directions in that 
        order : Left, Forward, Right.
        IGL stands for I Go Left.

        Parameters
        ----------
        position : tuple
            Coordinates of the current cell the runner is on.
        prev_position : tuple
            Previous position of the runner.
        neighbors : list of tuple
            Coordinates of the neighboring cells from the current position.

        Returns
        -------
        tuple
            Coordinates of the first cell of the path the runner will take.
        list of tuple
            Coordinates of the other paths the runner could take later.

        """
        orientation_table = self.get_orientation(position, prev_position)
        ordered_directions = [k for k in orientation_table \
                                  if k in neighbors]
        #We just make sure that the directions provided by the 
        #mazy.get_orientation are actual paths.
        return ordered_directions.pop(), ordered_directions
    
    def IAE(self, position, neighbors):
        """
        IAE know where the exit is and will aim for it wherever there is an
        intersection.
        IAE stands for I Aim for the Exit.

        Parameters
        ----------
        position : tuple
            Coordinates of the current cell the runner is on.
        neighbors : list of tuple
            Coordinates of the neighboring cells from the current position.

        Returns
        -------
        tuple
            Coordinates of the first cell of the path the runner will take.
        list of tuple
            Coordinates of the other paths the runner could take later.

        """
        distance = [[sqrt((self.exit_point[0]-k[0])**2 + \
                             (self.exit_point[1]-k[1])**2), k] \
                             for k in neighbors]
        #The euclid distance between a coordinate from a neighbors and the 
        #exit point is processed. Each element of the distance list is a 
        #list that contains the euclid distance and the 
        #neighbor cell coordinates.
        movement = True
        while movement == True :
            movement = False
            for k in range(1, len(distance)):
                if distance[k-1][0] < distance[k][0]:
                    distance[k-1], distance[k] = distance[k], distance[k-1]
                    movement = True
        #We bubble sort the euclid distance from the longest to the smallest.
        choice = distance.pop()[1]
        return choice, [k[1] for k in distance]
            
        
    def runner_selector(self, runner, position, prev_position, neighbors):
        """
        Simply run the given runner algorithm.

        Parameters
        ----------
        runner : str
            Name of the runner.
        position : tuple
            Coordinates of the current cell the runner is on.
        prev_position : tuple
            Previous position of the runner.
        neighbors : list of tuple
            Coordinates of the neighboring cells from the current position.

        Returns
        -------
        tuple
            Coordinates of the first cell of the path the runner will take.
        list of tuple
            Coordinates of the other paths the runner could take later.

        """
        if runner == "ICR":
            return mazy.ICR(position, neighbors)
        elif runner == "IGR":
            return self.IGR(position, prev_position, neighbors)
        elif runner == "IGL":
            return self.IGL(position, prev_position, neighbors)
        elif runner == "IAE":
            return self.IAE(position, neighbors)
        
    def path_shower(self, paths, runner):
        """
        Color the maze. The brighter the color is the latest that path as been
        taken. It color the whole path (between 2 intersections) 
        with the same color.

        Parameters
        ----------
        paths : list of list
            Each sublist is a whole path (between 2 instersections).
        runner : str
            Name of the runner.

        Returns
        -------
        None.

        """
        value = 2
        for path in paths :
            self.maze.set_values(path, value)
            value += 1
            #The paths in the paths list is ordered from the earliest took path
            #to the latest took path
        self.maze.save(runner)
        #The maze grid is saved with its name.
        self.maze.display(colors="viridis")
        self.maze.grid = self.maze.saved["Original"]
        #The maze grid is set back to the clean and original maze in order to 
        #continue working with it.
        

    def maze_runner(self, runner="ICR"):
        """
        Algorithm to solve the maze

        Parameters
        ----------
        runner : str, optional
            Name of the runner. The default is "ICR".

        Returns
        -------
        None.

        """
        position = self.start_point
        #position is a tuple with the coordinates of 
        #the current position of the runner. 
        path = [[position]]
        #List of all the taken paths where each sublist is a whole path between
        #2 intersections.
        explored = []
        #List of all explored cells' coordinates. 
        intersections = []
        #List of available coordinates of the first cell of explorable paths.
        prev_position = (0, 1)
        #tuple with the coordinates of the previous position the runner was.
        while position != self.exit_point:
            #The runner continues to explore while he hasn't get to 
            #the exit_point 
            neighbors_raw = self.path_neighbors[position]
            #Raw list of the neighboring cells from the current position.
            #Those neighbors are paths but they could've been already explored.
            neighbors = [k for k in neighbors_raw if k not in explored]
            #neighbors_raw list filtered as only the unexplored cells remains.
            neighbors_count = len(neighbors)
            #Number of possibilities for the runner to choose.
            explored.append(position)
            if neighbors_count == 0:
                #Deadend so the runner goes back to the last intersection.
                path[-1].append(position)
                prev_position, position = position, intersections.pop()
                path.append([position])
                #New sublist in path as the runner will take a new path.
            elif neighbors_count > 1:
                #Intersections so the runner algorithm 
                #has to choose a direction
                choice, options = self.runner_selector(runner, position, \
                                                     prev_position, neighbors)
                #choice is the first cell of the path that the runner 
                #will take. options is the list of other path the runner could 
                #take.
                path[-1].append(position)
                #The current position is saved in the current path sublist.
                path.append([choice])
                #The next position (called choice) is added in a new sublist.
                intersections += options
                #The other paths first cell coordintes are added to the list 
                #of intersections.
                prev_position, position = position, choice
                #The runner move so we update the current and previous 
                #position.
            else :
                #There are no intersection neither deadend so the runner 
                #continues down the path.
                path[-1].append(position)
                prev_position, position = position, neighbors[0]
                #The current and previous position are updated.
        self.path_shower(path, runner)
        #The journey of the runner is shown and saved.
        self.runner_path[runner] = {"Explored": explored, "Path": path,\
                                    "Distance": len(explored)}
        #The explored cells, the paths that were taken and the total 
        #cell-distance travelled by the runner are saved in the 
        #self.runner_path dictionnary.
        
    def summary(self):
        """
        Give a summary on the maze.

        Returns
        -------
        None.

        """
        print("")
        print("There are {} path cells in the maze.".format(len(self.drilled)))
        print("")
        print("The quickest path to the exit takes {} steps.".format(\
              self.start_distance))
        print("")
        for k in self.runner_path:
            print(k,"has made it to the exit in {} steps.".format(\
                  self.runner_path[k]["Distance"]))






if __name__ == "__main__":
    maze = mazy(mode="fast")
    maze.maze_runner("ICR")
    maze.maze_runner("IGR")
    maze.maze_runner("IGL")
    maze.maze_runner("IAE")
    maze.summary()