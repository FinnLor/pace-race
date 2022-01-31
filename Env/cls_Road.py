# -*- coding: utf-8 -*-
"""
Created on Dec 2021

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""


from shapely.geometry import LineString, Point
from scipy.interpolate import interp1d 
import numpy as np


class Road:
    """
    
    Class to represent a roadway in R2. 
    All physical quantities are to be interpreted in Si base units.
    
    ...
    
    Attributes
    ----------
    center_line : shapely.geometry.LineString
        Trajectory of the lane centerline.
    left_line : shapely.geometry.LineString
        Trajectory of the left lane boundary.
    right_line: shapely.geometry.LineString
        Trajectory of the right lane boundary.
    ROADWIDTH : int or float 
        Width of the roadway.
    
    Methods
    -------
    get_path_length(xy, normalized = True): 
        Returns the relative (default) or absolute distance from the first point of the road to a specified point, 
        measured along the lane centerline.
        
    """


    def __init__(self, ROADWIDTH=8, ROADLENGTH: int = 10, NPOINTS: int = 1000, 
                 custom_center_line = None):
        """
        
        Initializes object.
        Creates a simple, randomly parameterized, or custom trajectory in R2, which is set as the lane centerline (self. center_line). 
        The left and right lane boundaries (self.left_line and self.right_line) are derived using the width of the roadway (self.ROADWIDTH).

        ...

        Parameters
        ----------
        ROADWIDTH : int or float, optional
            Width of the roadway. Non-negative value. The default is 8.
        ROADLENGTH : int, optional
            Discrete factor for length of random road. Valid inputs: {2, 3, 4, 5, 6, 7, 8, 9, 10}. The default is 10.
        NPOINTS : int, optional
            Number of points used to define the lane centerline, when ROADLENGTH >  and custom_center_line = None. The default is 1000.
        custom_center_line : np.ndarray with size [nx2], optional
            Custom trajectory in R2 [x,y]-value-pairs. The default is None.

        Returns
        -------
        None.

        """
        
        # Check inputs
        assert ROADWIDTH >= 0, "ROADWIDTH has to be non-negative!"
        
        # Random road
        if custom_center_line is None:
            # Check inputs for random road
            valid_ROADLENGTH = {2, 3, 4, 5, 6, 7, 8, 9, 10}
            if ROADLENGTH not in valid_ROADLENGTH:
                raise ValueError("ROADLENGTH must be one of %r." % valid_ROADLENGTH)
            
            # Generate random road
            x = np.cumsum(np.random.rand(ROADLENGTH)+0.3)*10*ROADLENGTH 
            y = np.cumsum((np.random.rand(ROADLENGTH)-0.5)*2)*10*ROADLENGTH               
            if ROADLENGTH < 3:
                f = interp1d(x, y, kind='linear')
                x = np.linspace(x[0], x[ROADLENGTH-1], 2)
            else: 
                f = interp1d(x, y, kind='quadratic')
                x = np.linspace(x[0], x[ROADLENGTH-1], NPOINTS)
            y = f(x)
            line_data = np.transpose([x,y])
        # Custom road
        else:              
            assert (isinstance(custom_center_line,np.ndarray) and
                    custom_center_line.ndim == 2 and
                    custom_center_line.shape[1] == 2) , "custom_center_line has to be [nx2] np.ndarray!"
            line_data = custom_center_line
        
        # Assign properties
        self.ROADWIDTH = ROADWIDTH
            
        # Generate lane centerline and lane boundaries.
        self.center_line = LineString(line_data)
        self.left_line = self.center_line.parallel_offset(self.ROADWIDTH/2,"left",join_style=1)
        self.right_line = self.center_line.parallel_offset(self.ROADWIDTH/2,"right",join_style=1)
        

    def get_path_length(self, xy, normalized = True): # call with car.center
        """
        
        Returns the relative (default) or absolute distance from the first point of the road to a specified point, 
        measured along the lane centerline.

        Parameters
        ----------
        xy : array or list with two elements
            Coordinates in R2.
        normalized : bool, optional
            Information whether the length should be scaled to [0, 1]. The default is True.

        Returns
        -------
        path_length : float
            Distance from the first point of the road to the specified point.
            
        """
        
        p = Point(xy)
        path_length = self.center_line.project(p, normalized = normalized)
        return path_length


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # Create object
    road = Road(ROADLENGTH = 3)
        
    # Get data from object
    x_center_line = np.array(road.center_line.coords)[:,0] 
    y_center_line = np.array(road.center_line.coords)[:,1] 
    x_left_line = np.array(road.left_line.coords)[:,0] 
    y_left_line = np.array(road.left_line.coords)[:,1] 
    x_right_line = np.array(road.right_line.coords)[:,0] 
    y_right_line = np.array(road.right_line.coords)[:,1] 
    
    # Define points
    p1 = [100,100] # list
    p2 = np.array([-100,-100]) # numpy-array
    
    # Visualize
    plt.plot(x_center_line, y_center_line, label='center_line')
    plt.plot(x_left_line, y_left_line, label = 'left_line')
    plt.plot(x_right_line, y_right_line, label = 'right_line')
    plt.scatter(p1[0], p1[1], linewidths=5, label = 'p1')
    plt.scatter(p2[0], p2[1], linewidths=5, label = 'p2')
    plt.legend()

    # Get lenght
    path_length1 = road.get_path_length(p1, normalized = False)
    print(path_length1)
    path_length2 = road.get_path_length(p2)
    print(path_length2)