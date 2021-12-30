# -*- coding: utf-8 -*-
"""
Created on Dec 2021

@author: Finn Lorenzen, Eliseo Milonia, Felix Schönig
"""

from shapely.geometry import LineString, Point, Polygon
from shapely.errors import ShapelyDeprecationWarning
import numpy as np
import math
from scipy import integrate
import warnings


def _rot_mat(angle):
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    

class Car:
    """
    
    Class to represent a car in R2 including geometrie in dynamics. 
    All physical quantities are to be interpreted in Si base units.
    
    ...
    
    Attributes
    ----------
    work in progress
    
    Methods
    -------
    work in progress
        
    """
    
    
    def __init__(self, LF=2, LR=2, WIDTH=2, M=2_000, P=100_000,\
                 x=0, y=0, psi=0, delta=0, SENS_SCALE=1):
        """
        
        Initializes object.
        Creates a car consisting of 
            - geometry defined by points c1 to c5 (see below), 
            - information about direction and range of sensors s01 to s09 (see below)
            - information about power and vehicle mass. 
        The position of the car is defined via coordinates (x and y), 
        as well as the specification of yaw angle and steering angle in R2. 
        
            Geometrie overview
            ------------------
        
            W    c1-----------------c5
            I    |                  | \        
            D    |<-LR-> x/y <-LF-> | c4    ---> v
            T    |                  | /     
            H    c2-----------------c3
        
                y
                ^
                |
                ---> x
        
            Sensor overview
            ---------------
        
              s01  s03
              |  / 
              c4 --- s05
              |  \
             s09  s07
        
        ...

        Parameters
        ----------
        LF : int or float, optional
            Distance from center to front wheel. Non-negative value. The default is 2.
        LR : int or float, optional
            Distance form center to rear wheel. Non-negative value. The default is 2.
        WIDTH : int or float, optional
            Width of car. Non-negative value. The default is 2.
        M : int or float, optional
            Mass of car. Non-negative value. The default is 2_000.
        P : int or float, optional
            Power of car. Non-negative value. The default is 100_000.
        x : int or float, optional
            x-Position of the car center point. The default is 0.
        y : int or float, optional
            y-Position of the center point. The default is 0.
        psi : int or float, optional
            Yaw angle. The default is 0.
        delta : int or float, optional
            DESCRIPTION. The default is 0.
        SENS_SCALE : int or float, optional
            Steering angle. The default is 1.

        Returns
        -------
        None.

        """

        # Check inputs
        assert LF >= 0 , "LF has to be non-negative!"
        assert LR >= 0 , "LR has to be non-negative!"
        assert WIDTH >= 0 , "WIDTH has to be non-negative!"
        assert M >= 0 , "M has to be non-negative!"
        assert P >= 0 , "P has to be non-negative!"
        
        # Assign geometric Properties
        self.LF = LF
        self.LR = LR
        self.WIDTH  = WIDTH # car width
        self.SENS_SCALE = SENS_SCALE
        
        # Set car position 
        self.set_car_pos(x, y, psi, delta)
                
        
    def set_car_pos(self, x, y, psi, delta):
        """
        
        Sets the car to a specified position in the R2.
        
        ...

        Parameters
        ----------
        x : int or float
            x-Position of the car center point.
        y : int or float
            y-Position of the car center point.
        psi : int or float
            Yaw angle.
        delta : int or float
            Steering angle.

        Returns
        -------
        None.

        """
        
        # Set center-point of car
        self.center = np.array([x, y])
        
        # Get rotation matrices
        rot_car = _rot_mat(psi)
        rot_sensor = _rot_mat(psi+delta)
               
        # Set corners of car
        c1 = self.center + np.dot(rot_car, (-self.LR, + self.WIDTH/2) )
        c2 = self.center + np.dot(rot_car, (-self.LR, - self.WIDTH/2) )
        c3 = self.center + np.dot(rot_car, (+self.LF, - self.WIDTH/2) )
        c5 = self.center + np.dot(rot_car, (+self.LF, + self.WIDTH/2) )
        
        # ... and position of sensor
        c4 = self.center + np.dot(rot_car, (1.5*self.LF, 0) )
             
        # Summarize all vertices of car in an array and assign to object
        self.corners = np.vstack((c1,c2,c3,c4,c5))
           
        # Set sensor end-points
        s01 = c4 + np.dot(rot_car, (0, self.WIDTH) )
        s03 = c4 + np.dot(rot_sensor, (self.SENS_SCALE*15, self.WIDTH) )
        s05 = c4 + np.dot(rot_sensor, (self.SENS_SCALE*60, 0) )
        s07 = c4 + np.dot(rot_sensor, (self.SENS_SCALE*15, -self.WIDTH) )
        s09 = c4 + np.dot(rot_car, (0, -self.WIDTH) )
        
        # Assign position of sensor to object
        self.s_ref = c4
        
        # Summarize all sensor end-points in an array and assign to object
        self.sensors = np.vstack((s01,s03,s05,s07,s09))
        
                
    def set_start_pos(self, road):    
        """
        
        Sets the car to the starting point of a road (on centerline). 
        The car is aligned tangentially to the lane centerline. 
        The steering angle is set to 0 rad.
        
        ...

        Parameters
        ----------
        road : Road
            Road-object defined in cls_Road.

        Returns
        -------
        None.

        """
        
        path = np.array(road.center_line.coords)  
        x = path[0, 0]
        y = path[0, 1]     
        dx = path[1, 0] - x
        dy = path[1, 1] - y
        psi = np.arctan2(dy, dx)
        self.set_car_pos(x, y, psi, 0) # x, y, psi, delta
     
                  
    def set_resume_pos(self, road):  
        """
        
        Sets the car on the center line at the shortest distance from the current position.  
        The car is aligned tangentially to the lane centerline. 
        The steering angle is reset to 0 rad.
        
        ...

        Parameters
        ----------
        road : Road
            Road-object defined in cls_Road.

        Returns
        -------
        None.

        """
        
        # Define shapely-object from car center-point 
        p = Point(self.center)
        
        # Get pathlength along the centerline to the shortest distance to P
        path_length = road.center_line.project(p, normalized = False) 
        
        # Find resume-position using pathlength
        resume_pos = np.asarray(road.center_line.interpolate(path_length).coords.xy).squeeze()

        # Find normal direction of centerline at the resume-position
        normal_direction = (self.center-resume_pos)  

        # Find out whether normal vector must be rotated by -pi/2 or +pi/2 for continuous direction
        dist_to_left_side = p.distance(road.left_line) 
        dist_to_right_side = p.distance(road.right_line)
        if dist_to_left_side > dist_to_right_side:
            add_to_psi = np.pi/2
        elif dist_to_left_side < dist_to_right_side:
            add_to_psi = -np.pi/2
        else:
            print("Check whether car is already set to start or resume position. Can't calculate psi.")      
         
        # Find psi
        psi = np.arctan2(normal_direction[1], normal_direction[0])+add_to_psi
        
        # Set car-position
        self.set_car_pos(resume_pos[0], resume_pos[1], psi, 0) # x, y, psi, delta

           
    def get_path_length(self, road, normalized = True): 
        """
        
        Find the reached distance measured along the centerline.
        
        ...

        Parameters
        ----------
        road : Road
            Road-object defined in cls_Road.
        normalized : bool, optional
            Specifies whether the distance should be related to the total length of the road. The default is True.

        Returns
        -------
        path_length : float
            Reached distance measured along the centerline (relative or absolute).

        """
                
        p = Point(self.center)
        path_length = road.center_line.project(p, normalized = normalized)
        return path_length


    def collision_check(self, road): 
        """
        
        Checks whether the vehicle is still on the road. 
        If the vehicle intersects one of the boundary lines or is outside the road, 
        False is returned, otherwise True.
        
        ...
        
        Parameters
        ----------
        road : Road
            Road-object defined in cls_Road.

        Returns
        -------
        collision : bool
            Indication whether collision has occurred.

        """
        
        # Old approach. Does not cover all cases.
        # max_dist = 0
        # for row in self.corners:
        #     dist = road.center_line.distance(Point(row))
        #     max_dist = max(max_dist, dist)
   
        # # check if car exceeds border
        # if max_dist >= road.ROADWIDTH/2:
        #     collision = True
        # else:
        #     collision = False
        
        # Get coordinates of left and right lane boundaries 
        left_line_coords = np.array(road.left_line.coords)
        right_line_coords = np.array(road.right_line.coords)
        
        # Extrapolate the boundaries linearly at the starting point of the road.
        ds_left = left_line_coords[[0],:]-left_line_coords[[1],:]
        ds_right = right_line_coords[[-1],:]-right_line_coords[[-2],:]
        extrapolation_start_left_line = left_line_coords[[0],:]+ds_left/np.linalg.norm(ds_left)*self.LR*1.1
        extrapolation_start_right_line = right_line_coords[[-1],:]+ds_right/np.linalg.norm(ds_right)*self.LR*1.1
        
        # Extrapolate the boundaries linearly at the end point of the road.
        ds_left = left_line_coords[[-1],:]-left_line_coords[[-2],:]
        ds_right = right_line_coords[[0],:]-right_line_coords[[1],:]
        extrapolation_end_left_line = left_line_coords[[-1],:]+ds_left/np.linalg.norm(ds_left)*self.LF*3
        extrapolation_end_right_line = right_line_coords[[0],:]+ds_right/np.linalg.norm(ds_right)*self.LF*3
        
        # Create a polygon-object of the extended road.
        extended_road_polygon = Polygon(np.concatenate((extrapolation_start_left_line,\
                                               left_line_coords,\
                                               extrapolation_end_left_line ,\
                                               extrapolation_end_right_line,\
                                               right_line_coords,\
                                               extrapolation_start_right_line),\
                                               axis=0))
         
        # Create a polygon-object of the car. 
        car_polygon = Polygon(self.corners)
        
        # Check if the intersection area is 1.
        collision = car_polygon.intersection(extended_road_polygon).area != car_polygon.area
        
        ###  For debugging. Please don't delete yet.
        # fig99, ax99 = plt.subplots()
        # data = np.array(extended_road_polygon.exterior.coords.xy)
        # ax99.plot(data[0,:], data[1,:], label='extended_road')
        # ax99.scatter(self.center[0], self.center[1], label = 'car_center')
        # ax99.scatter(self.corners[:,0], self.corners[:,1], label = 'car_corners')
        # ax99.scatter(left_line_coords[-1,0], left_line_coords[-1,1], label = 'end_of_road_left')
        # ax99.scatter(right_line_coords[0,0], right_line_coords[0,1], label = 'end_of_road_right')
        # ax99.legend()
        
        # print('Car')
        # print(car_polygon.area)
        # print('Intersec')
        # print(car_polygon.intersection(extended_road_polygon).area)
        
        return collision


    def get_sensordata(self, road, normalized = True):
        """
        
        Find out whether there is one of the boundaries in the sensors' field of view. 
        If True, return the distance, if False return the max. measuring range.
        
        ...

        Parameters
        ----------
        road : Road
            Road-object defined in cls_Road.
        normalized : bool, optional
            Specifies whether the distance should be related to the total length of the sensors' measuring range.
            The default is True.

        Returns
        -------
        dist : float
            Array of the measured distances (relative or absolute).
            1. column: intersections with the left boundary 
            2. column: intersections with the right boundary 
            rows: sensors

        """
        
        # Preallocate
        dist = np.ones(np.shape(self.sensors)) # col0: left, col1:right
        
        # Counter
        idx = 0
        
        # Reference point, source of all sensor lines as Point-object
        sensor_ref = Point(self.s_ref) 
        
        # Iterate on the sensors.
        for row in self.sensors:
            # Define sensor-line
            sensor_line = LineString(np.vstack((self.s_ref, row)))
            # Get length of line and set as max. measuring range
            sensor_length = sensor_line.length
            dist[idx, :] = sensor_length
            
            # Check for intersections with the boundaries
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
                # Suppresses the warning
                #   ShapelyDeprecationWarning: The array interface is deprecated and will no longer 
                #   work in Shapely 2.0. Convert the '.coords' to a numpy array instead.
                # because the proposed solution does not work when multiple points are returned.
                intersec_left = np.array(sensor_line.intersection(road.left_line))   
                intersec_right = np.array(sensor_line.intersection(road.right_line))
            if np.size(intersec_left) == 2:
                intersec_left = np.reshape(intersec_left, [1,2])
            if np.size(intersec_right) == 2:
                intersec_right = np.reshape(intersec_right, [1,2])
            
            # If there is more than on intersection find the lentht to the closest.
            for intersec_l in intersec_left:
                dist[idx, 0] = min(dist[idx, 0], sensor_ref.distance(Point(intersec_l)))
                
            for intersec_r in intersec_right:
                dist[idx, 1] = min(dist[idx, 1], sensor_ref.distance(Point(intersec_r))) 
            
            # Resize sensor distances due to the max length of the sensorline
            if normalized == True:
                dist[idx, :] = dist[idx, :]/sensor_length
            
            idx += 1
           
        return dist


    def _car_dynamics(self, t, states, action):
        a, delta = action
        x, y, psi, vlon, vlat, omega = states
        R = (self.LF+self.LR)/math.tan(delta) * 1/(math.atan(math.tan(delta) * self.LR/(self.LF+self.LR)))
        JZ = self.M *R^2


        # dxdt = vlon*math.cos(psi) - vlat*math.sin(psi)
        # dydt = vlon*math.sin(psi) + vlat*math.cos(psi)
        # dpsidt = omega
        # dvlondt = a
        # dvlatdt = -omega*vlon + 1/self.M* (-self.CR*math.atan2(vlat-omega*self.LR, vlon) -math.cos(delta)*self.CF*math.atan2(-vlon*math.sin(delta)+math.cos(delta)*vlat+math.cos(delta)*omega*self.LF, vlon*math.cos(delta)+math.sin(delta)*vlat+math.sin(delta)*omega*self.LF))
        # domegadt = 1/self.JZ * (self.CR*self.LR*math.atan2(vlat-omega*self.LR, vlon) -self.CF*self.LF*math.atan2(-vlon*math.sin(delta)+math.cos(delta)*vlat+math.cos(delta)*omega*self.LF, vlon*math.cos(delta)+math.sin(delta)*vlat+math.sin(delta)*omega*self.LF))

        pass #return dxdt, dydt, dpsidt, dvlondt, dvlatdt, domegadt

    def get_next_car_position(self, obervations, action):
        # # Run one timestep of the environment's dynamics
        # res = integrate.solve_ivp(fun=model, t_span=(self.t0, self.t0+self.cycletime), \
        #                           y0=np.array(self.state), args=[action], \
        #                           t_eval=np.linspace(self.t0, self.t0+self.cycletime, 10))
        # self.state = np.array(res.y[0:6,-1], dtype=np.float32)    # UPDATE STATES
        # self.t0 = self.t0+self.cycletime

        # # return forces
        # a, delta = action # unpack the action variables, because delta is needed
        # omega_after_int = res.y[5,-1] # get current angle velocity
        # try:
        #     R = (self.LF+self.LR)/math.tan(delta) * 1/(math.atan(math.tan(delta) * self.LR/(self.LF+self.LR)))
        #     F_ctfg = self.M * omega_after_int**2 * R # centrifugal force
        # except ZeroDivisionError:
        #     F_ctfg = 0
        
        pass #return new_observation
        
    
        

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from cls_Road import Road

    # Create car-objects
    car1 = Car()
    car2 = Car(LF=1, LR=1, WIDTH=1, x=15, y=-4, psi=np.pi/4, delta=-np.pi/4, SENS_SCALE=1)
    
    # Visualize car1. CAUTION: axis are not equal! 
    fig1, ax1 = plt.subplots()
    ax1.scatter(car1.center[0], car1.center[1], label = 'car1_center')
    ax1.scatter(car1.corners[:,0], car1.corners[:,1], label = 'car1_corners')
    ax1.scatter(car1.sensors[:,0], car1.sensors[:,1], label = 'car1_sensors')
    ax1.legend()
    fig1.suptitle('Position of car1')
    
    # Visualize car2. CAUTION: axis are not equal! 
    fig2, ax2 = plt.subplots()
    ax2.scatter(car2.center[0], car2.center[1], label = 'car2_center')
    ax2.scatter(car2.corners[:,0], car2.corners[:,1], label = 'car2_corners')
    ax2.scatter(car2.sensors[:,0], car2.sensors[:,1], label = 'car2_sensors')
    ax2.legend()
    fig2.suptitle('Position of car2')

    # Set car1 to new position
    car1.set_car_pos(-2, 1, -np.pi/2, np.pi/4) # x, y, psi, delta
    
    # Visualize new position of car1. CAUTION: axis are not equal! 
    fig3, ax3 = plt.subplots()
    ax3.scatter(car1.center[0], car1.center[1], label = 'car1_center')
    ax3.scatter(car1.corners[:,0], car1.corners[:,1], label = 'car1_corners')
    ax3.scatter(car1.sensors[:,0], car1.sensors[:,1], label = 'car1_sensors')
    ax3.legend()
    fig3.suptitle('New Position of car1')

    # Create road-object
    road = Road()
    
    # Get data from road
    x_center_line = np.array(road.center_line.coords)[:,0] 
    y_center_line = np.array(road.center_line.coords)[:,1] 
    x_left_line = np.array(road.left_line.coords)[:,0] 
    y_left_line = np.array(road.left_line.coords)[:,1] 
    x_right_line = np.array(road.right_line.coords)[:,0] 
    y_right_line = np.array(road.right_line.coords)[:,1] 
    
    # Visualize Road
    fig4, ax4 = plt.subplots()
    ax4.plot(x_center_line, y_center_line, label='center_line')
    ax4.plot(x_left_line, y_left_line, label = 'left_line')
    ax4.plot(x_right_line, y_right_line, label = 'right_line')
    
    # Set car1 to start-position of road
    car1.set_start_pos(road)  

    # Add car1 to current figure
    ax4.scatter(car1.center[0], car1.center[1], label = 'car1_center')
    ax4.scatter(car1.corners[:,0], car1.corners[:,1], label = 'car1_corners')
    ax4.scatter(car1.sensors[:,0], car1.sensors[:,1], label = 'car1_sensors')
    ax4.legend()
    fig4.suptitle('Road and car1 on start-position')       
        
    # Set car2 from new position next to road to resume-position
    car2.set_car_pos(x_center_line[100], y_center_line[100]+40, np.pi, 0)
    car2.set_resume_pos(road)
    
    # Add car2 to current figure
    ax4.scatter(car2.center[0], car2.center[1], label = 'car2_center')
    ax4.scatter(car2.corners[:,0], car2.corners[:,1], label = 'car2_corners')
    ax4.scatter(car2.sensors[:,0], car2.sensors[:,1], label = 'car2_sensors')
    ax4.legend()
    fig4.suptitle('Road and car1 on start-position & car2 on resume-position')   
    
    # Print reached path-lengths
    print(car1.get_path_length(road)) # relative
    print(car2.get_path_length(road, normalized= False)) # absolute
    
    # Collision checks
    print(car1.collision_check(road)) # False, car1 is on start-position
    car2.set_car_pos(car2.center[0], car2.center[1]+road.ROADWIDTH/2, 0, 0) # x, y, psi, delta
    print(car2.collision_check(road)) # True, intersection with boundary
    car2.set_car_pos(car2.center[0], car2.center[1]+road.ROADWIDTH*2, 0, 0) # x, y, psi, delta
    print(car2.collision_check(road)) # True, car2 out of roadway
    
    # Get sensor-data from car1
    print(car1.get_sensordata(road)) # relative distance
    print(car1.get_sensordata(road, normalized = False)) # absoluted distance
    
    





        
      