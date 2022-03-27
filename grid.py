# -*- coding: utf-8 -*-
"""
Grid generating class

@author: Alex-932
@Version : 1.0 (20/03/22)
"""
import numpy
import matplotlib.pyplot as plt

class Grid():
    """
    Generate numpy grids and provide methods to work with it.
    """
    
    def __init__(self, x, y, tor=False, value=0, dist="fixed", rep=.5):
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
        self._value = value
        self._tor = tor
        self.fig, self.ax = plt.subplots(figsize=(16, 16))
        self.neighbors = 1
        
        if self._dist == "fixed" and type(self._value) == int :
            self.grid = numpy.ones([self._y, self._x])*self._value
        elif self._dist == "random" and type(self._value) == list :
            self.grid = numpy.random.choice(
                self._value, size=[self._y, self._x], p=[(1-rep), rep])
        else :
            raise ValueError("Wrong set of parameters")
        self.saved = []
        self.coordinates()
    
    def set_value(self, coord, value):
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
        
    def get_value(self, x, y):
        """
        Method used to get the value of a cell.

        Parameters
        ----------
        x : (Int) x coordinates of the cell.
        y : (Int) y coordinates of the cell.

        Returns
        -------
        The value of the designated cell.

        """
        return self.grid[y, x]
    
    def get_neighbors(self, x, y, length=1):
        """
        Method to calculate the coordinates of neighbors cells.

        Parameters
        ----------
        x : (Int) x coordinates of the cell.
        y : (Int) y coordinates of the cell.
        length : (Int) Cell range for the search.

        Returns
        -------
        List of neighbors coordinates. 
        """
        list_neigh = []
        if x not in range(self._x) and y not in range(self._y):
            raise ValueError("Coordinates are not in the array") 
        for k in range(y-length, y+1+length):
            if k >= 0 and k < self.grid.shape[0] :
                for j in range(x-length, x+1+length):
                    if j >= 0 and j < self.grid.shape[1] and (k,j) != (y,x) :
                        list_neigh.append((j, k))
        return list_neigh
    
    def get_neighbors_tor(self, x, y, length=1):
        """
        Method to calculate the coordinates of neighbors cells similar to the 
        get_neighbors() method but consider the array as a toroidal space.

        Parameters
        ----------
        x : (Int) x coordinates of the cell.
        y : (Int) y coordinates of the cell.
        length : (Int) Cell range for the search.

        Returns
        -------
        List of neighbors coordinates. 
        """
        list_neigh = []
        if x not in range(self._x) and y not in range(self._y):
            raise ValueError("Coordinates are not in the array") 
        for k in range(y-length, y+1+length):
            for j in range(x-length, x+1+length):
                if (k,j) != (y,x) :
                    list_neigh.append((j%self._x, k%self._y))
        return list_neigh
    
    def get_neighbors_values(self, x, y):
        """
        Method similar to get_neighbors() but return a list of the values of 
        the surrounding cells.

        Parameters
        ----------
        x : (Int) x coordinates of the cell.
        y : (Int) y coordinates of the cell.

        Returns
        -------
        List of neighbors values.
        """
        return [self.grid[y, x] for (x, y) in self.neighbors[str((x, y))]]
        
    def show_neighbors(self, x, y, length=1):
        """
        Method to color the neighboring cells and show them.

        Parameters
        ----------
        x : (Int) x coordinates of the cell.
        y : (Int) y coordinates of the cell.
        length : (Int) Cell range for the search.

        Returns
        -------
        None.
        """
        if self._neighbors_length == length :
            list_neigh = self.neighbors[str((x, y))]
        elif self._tor :
            list_neigh = self.get_neighbors_tor(x, y, length)
        else :
            list_neigh = self.get_neighbors_tor(x, y, length)    
        self.set_value(list_neigh, 100)
        self.display()
        
    def save(self):
        """
        Method intended to save the current grid into a list containing other 
        saved grid called "saved". To retrieve that list, just type 
        "<object>.saved".

        Returns
        -------
        None.
        """
        self.saved.append(self.grid.copy())
        
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
        
    def compute_neighbors(self, length=1):
        """
        Compute all the neighboring of all the cell of the array.
        
        Parameters
        ----------
        length : (Int) Cell range for the search.

        Returns
        -------
        None.

        """
        self._neighbors_length = length
        self.neighbors = {}
        if self._tor :
            for (x, y) in self.coord:
                list_neigh = self.get_neighbors_tor(x, y, length)
                self.neighbors[str((x, y))] = list_neigh
        else :
            for (x, y) in self.coord:
                list_neigh = self.get_neighbors(x, y, length)
                self.neighbors[str((x, y))] = list_neigh
                
    def save_fig(self, name):
        """
        Save the current grid as an image.

        Parameters
        ----------
        name : (Str) Name of the ouput file.

        Returns
        -------
        None.

        """
        self.display()
        # plt.imshow(self.grid)
        # plt.axes.get_xaxis().set_visible(False)
        # plt.axes.get_yaxis().set_visible(False)
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
                    coord_y = [k for k in range(new_y-offset, new_y+offset+1) if k >= 0 and k <= upscaled.shape[1]]
                    coord_x = [k for k in range(new_x-offset, new_x+offset+1) if k >= 0 and k <= upscaled.shape[0]]
                    for k in coord_y :
                        for j in coord_x :
                            upscaled[k, j] = 1
        return upscaled
        
if __name__ == "__main__":  # exécuté sauf si le module est importé
    t = Grid(10, 5)
    t.set_value([(0,0),(1,1),(2,2),(4,4)], 8)
    t.display()
    t.compute_neighbors(length=1)
    print(t.get_neighbors(2, 2))
    print(t.get_neighbors_values(2, 2))
    
