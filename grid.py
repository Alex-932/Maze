# -*- coding: utf-8 -*-
"""
Grid class to make working with numpy arrays much easier

@author: Alex-932
@Version : 2.1.1
"""
import numpy
import matplotlib.pyplot as plt
from datetime import datetime
import re

class grid():
    """
    Generate numpy grids and provide methods to work with it.
    """
    
    def __init__(self, x, y, tor=False, value=0, dist="fixed", rep=.5, \
                 file=''):
        """
        Initialize a grid with a size of x*y.

        Parameters
        ----------
        x : (Int) Size of the x axis of the space.
        y : (Int) Size of the y axis of the space.
        tor : (Bool) Consider the grid as a toroidal space.
        value : (List/Int) Values within the grid (1 or 2 values).
        dist : (Str) Distribution of the value within the grid.
        Parameters : "random", "fixed" (one value only)
        rep : (Float) Probability of having the first value of the value
        
        Returns
        -------
        The grid.
        """
        self._x = int(x)
        self._y = int(y)
        self._dist = str(dist)
        self._rep = float(rep)
        self._tor = tor
        self.fig, self.ax = plt.subplots(figsize=(16, 16))
        self.neighbors = 1
        if file != '':
            self._tor = tor
            self.import_file(file)
        elif self._dist == "fixed" and type(value) == int :
            self.grid = numpy.ones([self._y, self._x])*value
        elif self._dist == "random" and type(value) == list :
            self.grid = numpy.random.choice(
                value, size = [self._y, self._x], p=[(1-rep), rep])
        else :
            raise ValueError("Wrong set of parameters")
        self.saved = {}
        self.coordinates()
        
    def import_file(self, file):
        """
        Import a file

        Parameters
        ----------
        file : str
            File path.

        Returns
        -------
        None.

        """
        raw_file = open(file)
        raw_lines = raw_file.readlines()
        lines = [list(re.split('\n', k)[0]) for k in raw_lines]
        for sublist in lines :
            for index in range(len(sublist)) :
                sublist[index] = int(sublist[index])
        self._x = len(lines[0])
        self._y = len(lines)
        try :
            self.grid = numpy.array(lines)
        except :
             print("Something went wrong with the file !")
             
    def set_values(self, coord, value):
        """
        Set the value of the cells whose coordinates are in the coord list to 
        value.

        Parameters
        ----------
        coord : (List) list that contains the coordinates in the form of a 
        couple. For example : [(1,1),(3,5),...]
        value : (Float) Value the cells will have.

        Returns
        -------
        None
        """
        x, y = [],[]
        for j,k in coord:
            if j in range(self._x) and k in range(self._y) :
                x.append(j)
                y.append(k)
        self.grid[y, x] = value
        
    def get_values(self, coord):
        """
        Method used to get the value of one or more cell.

        Parameters
        ----------
        coord : tuple or list of tuples
            The tuple include the X and Y coordinates.

        Returns
        -------
        The value of the designated cell(s) as list.

        """
        if type(coord) == list:
            return [self.grid[y, x] for (x, y) in coord]
        elif type(coord) == tuple:
            return [self.grid[coord[1], coord[0]]]
    
    def get_neighbors(self, coord, length=1, pattern='O'):
        """
        Method to calculate the coordinates of neighbors cells.

        Parameters
        ----------
        coord : tuple
            The tuple include the X and Y coordinates.
        length : int
            Cell range for the search.
        pattern : chr
            Search pattern : "O" for a square area, "+" for a cross area.
            
        Returns
        -------
        List of neighbors coordinates. 
        """
        try :
            return self.neighbors[coord]
        except :
            list_neigh = []
            if length < 1 :
                raise ValueError("Incorrect length (must be >= 1)")
            if type(coord) != tuple and len(coord) != 2 :
                raise ValueError("Something is wrong with the coordinates")
            if coord[0] not in range(self._x) and \
                coord[1] not in range(self._y):
                raise ValueError("Some coordinates are not in the array")
            if pattern == 'O':
                for k in range(coord[1]-length, coord[1]+1+length):
                    if k >= 0 and k < self._y :
                        for j in range(coord[0]-length, coord[1]+1+length):
                            if j >= 0 and j < self._x \
                                and (k,j) != (coord[1],coord[0]) :
                                list_neigh.append((j, k))
            elif pattern == '+':
                modulation_list = [k for k in range(-length, length+1)\
                                   if k != 0]
                for k in modulation_list:
                    list_neigh.append((coord[0]+k,coord[1]))
                    list_neigh.append((coord[0],coord[1]+k))
            return list_neigh
    
    def get_neighbors_tor(self, coord, length=1, pattern='O'):
        """
        Method to calculate the coordinates of neighbors cells similar to the 
        get_neighbors() method but consider the array as a toroidal space.

        Parameters
        ----------
        coord : tuple
            The tuple include the X and Y coordinates.
        length : int
            Cell range for the search.
        pattern : chr
            Search pattern : "O" for a square area, "+" for a cross area.

        Returns
        -------
        List of neighbors coordinates. 
        """
        try :
            return self.neighbors[coord]
        except :
            list_neigh = []
            if length < 1 :
                raise ValueError("Incorrect length (must be >= 1)")
            if type(coord) != tuple and len(coord) != 2 :
                raise ValueError("Something is wrong with the coordinates")
            if coord[0] not in range(self._x) and coord[1] not in range(self._y):
                raise ValueError("Some coordinates are not in the array")
            if pattern == 'O':
                for k in range(coord[1]-length, coord[1]+1+length):
                    for j in range(coord[0]-length, coord[1]+1+length):
                        if (k,j) != (coord[1],coord[0]) :
                            list_neigh.append((j%self._x, k%self._y))
            elif pattern == '+':
                modulation_list = [k for k in range(-length, length+1) if k != 0]
                for k in modulation_list:
                    list_neigh.append(((coord[0]+k)%self._x, coord[1]%self._y))
                    list_neigh.append((coord[0]%self._x, (coord[1]+k)%self._y))
            return list_neigh
        
    def show_neighbors(self, coord):
        """
        Method to color the neighboring cells and show them.

        Parameters
        ----------
        coord : tuple
            The tuple include the X and Y coordinates.

        Returns
        -------
        None.
        """
        list_neigh = self.neighbors[coord]
        self.set_values(list_neigh, 100)
        self.display()
        
    def save(self, name):
        """
        Method intended to save the current grid into a list containing other 
        saved grid called "saved". To retrieve that list, just type 
        "<object>.saved".
        
        Parameters
        ----------
        name : str
            Name of the array that will be stored.    

        Returns
        -------
        None.
        """
        self.saved[name] = self.grid.copy()
        
    def coordinates(self):
        """
        Generate all the coordinates of the grid and save them in a list called
        "coord"

        Returns
        -------
        None.

        """
        self.coord = []
        for k in range(self._x):
            for j in range(self._y):
                self.coord.append((k,j))
        
    def compute_neighbors(self, length=1, pattern = 'O'):
        """
        Compute all the neighboring of all the cell of the array.
        
        Parameters
        ----------
        length : int
            Cell range for the search.
        pattern : chr
            Search pattern : "O" for a square area, "+" for a cross area.

        Returns
        -------
        None.

        """
        self._neighbors_length = length
        self.neighbors = {}
        if self._tor :
            for coord in self.coord:
                list_neigh = self.get_neighbors_tor(coord, length, pattern)
                self.neighbors[coord] = list_neigh
        else :
            for coord in self.coord:
                list_neigh = self.get_neighbors(coord, length, pattern)
                self.neighbors[coord] = list_neigh
                
    def display(self, grid_id="Current", colors="bone"):
        """
        Show the array as a graph.
        
        Parameters
        ----------
        grid : str
            Name of the grid in the self.saved dictionnary. 
            Default is "Current" which is the current grid.
        colors : str
            Color palette for the array.

        Returns
        -------
        None.

        """
        if grid_id == "Current" :
            plt.imshow(self.grid, cmap=colors, interpolation='nearest')
            plt.axis('off')
        else :
            try : 
                plt.imshow(self.saved[grid_id], cmap=colors, \
                           interpolation='nearest')
                plt.axis('off')
            except KeyError :
                print("The given grid name isn't in the saved grid !")
                print("Current grid is shown instead.")
                plt.imshow(self.grid, cmap=colors, interpolation='nearest')
                plt.axis('off')
        
    def save_fig(self, name):
        """
        Save the current grid as an image.

        Parameters
        ----------
        name : str
            Name of the ouput file.

        Returns
        -------
        None.

        """
        self.display()
        plt.savefig(name, dpi=200)
        
    def upscale(array, factor=3):
        """
        Upscale the array by the factor.

        Parameters
        ----------
        factor : Int, optional
            Upscaling factor. The default is 3.

        Returns
        -------
        The upscaled array.

        """
        upscaled = numpy.zeros([array.shape[0]*factor, array.shape[1]*factor])
        for y in range(array.shape[0]):
            for x in range(array.shape[1]):
                if array[y, x] == 1 :
                    new_y, new_x, offset = y*factor, x*factor, int(factor/2)
                    coord_y = [k for k in range(new_y-offset, new_y+offset+1) \
                               if k >= 0 and k <= upscaled.shape[1]]
                    coord_x = [k for k in range(new_x-offset, new_x+offset+1) \
                               if k >= 0 and k <= upscaled.shape[0]]
                    for k in coord_y :
                        for j in coord_x :
                            upscaled[k, j] = 1
        return upscaled
    
    def export(self, name):
        """
        Export the grid with the given name from the self.mazed dict in a 
        .txt file.

        Parameters
        ----------
        name : str
            Name of the grid in the self.saved dict.

        Returns
        -------
        None.

        """
        file = open("Maze_export_{}.txt".format(str(\
               datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))), "a")
        maze_as_list = self.saved["Original"].tolist()
        for raw_row in maze_as_list :
            raw_row = [str(int(k)) for k in raw_row]
            row = "".join(raw_row)
            file.write(row+'\n')
        file.close()
        
        
if __name__ == "__main__":
    t = grid(10, 5)
    t.set_values([(0,0),(1,1),(2,2),(4,4)], 8)
    t.display()
    t.compute_neighbors(length=1, pattern="+")
    print(t.get_neighbors((2, 2), pattern="+"))

    
