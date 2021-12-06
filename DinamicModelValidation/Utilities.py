# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:28:06 2020

@author: jasmi
"""
import numpy as np
# from scipy.spatial.transform import Rotation as R
# from math import atan2, sqrt

class Utilities:
    # --> Cross Checked with Modeling and simulation of aerospace Vehicle dynamics, P.H. Zipfel
    def euler_to_quaternion(yaw, pitch, roll):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return np.array([qx, qy, qz, qw])

    # --> Cross Checked with Modeling and simulation of aerospace Vehicle dynamics, P.H. Zipfel
    def quaternion_to_euler(x, y, z, w):

        import math
        # roll
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.atan2(t0, t1)
        
        # pitch
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.asin(t2)
        
        # yaw
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.atan2(t3, t4)



        return X, Y, Z


    def rk4_integrator(f, h, y0, t, args=()):
        # https://perso.crans.org/besson/notebooks/Runge-Kutta_methods_for_ODE_integration_in_Python.html        
        n = len(t)
        if n == 1:
            n=2
        y = np.zeros((n, len(y0)))
        y[0] = y0
        for i in range(n-1):
            h = t[i+1] - t[i]
            k1 = f( t[i], y[i], *args)
            k2 = f(t[i] + h / 2., y[i] + k1 * h / 2.,  *args)
            k3 = f(t[i] + h / 2., y[i] + k2 * h / 2.,  *args)
            k4 = f(t[i] + h, y[i] + k3 * h,  *args)
            if n == 2:
                y = y[i] + (h / 6.) * (k1 + 2*k2 + 2*k3 + k4)
            else:
                y[i+1] = y[i] + (h / 6.) * (k1 + 2*k2 + 2*k3 + k4)
                    
            
        return y
    
    def rk4_integrator_one_step(f, h, y0, t, args=()):
        """ f: function 
            h: time step [s]
            y0: initial states vector
            t : time at evaluation [s]
            args(): arguments for the functions
        """
        # https://perso.crans.org/besson/notebooks/Runge-Kutta_methods_for_ODE_integration_in_Python.html        
        y = np.zeros(len(y0))
        y = y0

        k1 = f( t, y, *args)
        k2 = f(t + h / 2., y + k1 * h / 2.,  *args)
        k3 = f(t + h / 2., y + k2 * h / 2.,  *args)
        k4 = f(t + h, y + k3 * h,  *args)
        y = y + (h / 6.) * (k1 + 2*k2 + 2*k3 + k4)
        # y = y+k1*h

        return y
    
    def rescale_to_interval (x, lower = 0, upper = 1):
        xMin = min(x)
        xMax = max(x)
        # slope = (upper-lower)/(xMax-xMin)
        y = np.zeros(len(x))
        for i in range (0,2):
            y[i] = (x[i]-xMin)/(xMax-xMin)*(upper-lower)+lower
        
        return y
    
    def wraptopi(x):
        pi = np.pi
        x = x - np.floor(x/(2*pi)) *2 *pi
        return x[x >= pi] - 2*pi
    
    #sigmoid function
    def sigmoid(X):
        return 1/(1+np.exp(-X))
    
    def sigmoid_derivative(x):
        s = Utilities.sigmoid(x)
        ds = s*(1-s)
        return ds
    
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx
