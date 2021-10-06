# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 17:16:00 2020

@author: Jasmine Rimani
Actuator Model and GNC for the rover
Main Ref: Development of a Mobile Robot Test Platform and Methods forValidation of Prognostics-Enabled Decision Making Algorithms, E. Balabam et al

"""


import numpy as np
from scipy.spatial.transform import Rotation as R
from math import atan2, sqrt
from planet import Earth
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from Utilities import Utilities 



class Dynamics():
    def Rover_Kinodynamics(t,y, F,M, M_wheels, I, m, 
                           L_motor, V_motor, R_motor, i_motor, K_e, omega_motor,Jm_motor, K_t,b_motor, eps_motor):

        """
        In y: 
         x,y,z: rover position in space [m] inertial reference system
         phi,theta,psi: rover angular position in space [rad] inertial reference system
         u,x,w : rover velocities in body ref frame [m/s]
         p,q,r: rover angular rate in body ref frame [rad/s]
         i_motor : current in the motor A]
         omega_motor: motor speed [m/s]
         
        inputs:
         F = Force on the Body
         M = Moment on the Body
         M_wheels = Total torque on the wheels
         I = Body Inertia matrix
         m = Body Mass
         L_motor = Motor Indutance
         V_motor = Motor entry voltage - evaluated with a PID as f(velocity) or f(position)
         R_motor = Motor Resistence
         i_motor = Motor Current (evaluated step by step)
         K_e = Eletromagnetic costant of the motor.
         omega_motor = velocity of the motor/wheel
         Jm_motor = moment of inertia motor 
         K_t = Torque Costant of the motor
         b_motor = Viscous torque
         eps_motor = efficiency of the motor 

        """
        
        # Rotation Matrix between Body and Inertia--> Rotation Convention 'ZYX' [adim]
        # R_BW = R.from_euler('zyx',[psi_rover, theta_rover, phi_rover])
        # R_BW = R_BW.as_matrix()
        # R_BW = R_BW.reshape(3,3)
        
        # You need quaterions to have a good rotation matrix
        phi_rover = y[3]
        theta_rover = y[4]
        psi_rover = y[5]
        q_rover = Utilities.euler_to_quaternion(psi_rover, theta_rover, phi_rover)
        
        # Matric between body and inertial frame --> (x,y)_inertial = M_rotation*(x,y)_body
        R_BW = R.from_quat(q_rover)
        R_BW = R_BW.as_matrix()
        R_BW = R_BW.reshape(3,3) 
        
        
        # Rotation matrix between body rates and inertial angular rates [adim]
        R_BW_eta = np.array([[1, np.sin(phi_rover)*np.tan(theta_rover), np.cos(phi_rover)*np.tan(theta_rover)],
                             [0, np.cos(phi_rover), -np.sin(phi_rover)],
                             [0, np.sin(phi_rover)*(1/np.cos(theta_rover)), np.cos(phi_rover)*(1/np.cos(theta_rover))]])


        # Velocities in body ref. frame [m/s] 
        v_body = np.array([y[6], y[7], y[8]])
        omega_body = np.array([y[9], y[10], y[11]])
        
        # Inertial Velocities in inertial ref. frame [m/s]  - you need the inertial values to use Newton Laws!!
        # To multiply use @ or np.dot
        v_inertial= R_BW@v_body
        # Inertial Angular Rates in inertial ref. frame [rad/s]
        eta_dot_inertial = R_BW_eta@omega_body
        # Linear Accelerations in body reference frame [m/s] --> Cross Checked with Modeling and simulation of aerospace Vehicle dynamics, P.H. Zipfel
        # v_dot=(1/m)*F-np.cross(omega_body,v_body)
        v_dot=(1/m)*F
        # Inverse rover Inertia matrix
        I_inv = np.linalg.inv(I)
        # Angular Accelerations in body reference frame [rad/s] --> Cross Checked with Modeling and simulation of aerospace Vehicle dynamics, P.H. Zipfel
        omega_body_dot=I_inv@M

        
        # Current and Motor speed --- from the AMES Model
        # V_motor = costant --> it's the voltage source
        i_motor_dot =np.zeros(4)
        for jj in range(0,4):
            i_motor_dot [jj] = (1/L_motor)*(V_motor[jj]-R_motor*i_motor[jj]-K_e*omega_motor[jj])

  
        # Current and Motor speed --- from the AMES Model
        omega_motor_dot =np.zeros(4)
        for jj in range(0,4):
            omega_motor_dot [jj] = (1/Jm_motor)*M_wheels[jj]
            

        # # Minimum stopping distance from an obstacle
        # self.min_dist_obstacle = (self.vel**2)/(2*self.acc)
        y=np.array([v_inertial,eta_dot_inertial,v_dot,omega_body_dot,i_motor_dot,omega_motor_dot, omega_motor])
        y=np.concatenate(y)
        
        return y



class Rover_Properties():
    def __init__(self):
        # Mass
        self.mass = 2.148 # kg
        # Moment of inertia about x-axis
        self.Ix = 0.0140 #kg*m^2
        # Moment of inertia about y-axis
        self.Iy = 0.0252 #kg*m^2
        # Moment of inertia about z-axis
        self.Iz = 0.0334 #kg*m^2
        # Radius of wheel
        self.radius_wheel = 0.0635 #m
        # Distance between the center of the two short side wheels
        self.b = 0.249
        # Distance between the center of two long side wheels
        self.l =0.446
        
        
        #  Effective area in x-axis
        self.Ax = 0.0316 #m^2
        #  Effective area in y-axis
        self.Ay = 0.0448 #m^2
        # Drag coefficient
        self.Cd = 0.89
        # Weight
        x_planet = Earth()
        self.weight = self.mass*(x_planet.g)
        # Moment arm of wheel
        self.moment_arm_wheel = 0.1245 # m --> look at the figure
        # Coefficient of friction in x
        self.sigma_x = 0.22
        # Coefficient of friction in y
        self.sigma_y = 1
        # Coefficient of friction in z
        self.sigma_z = 0.30
        # Coefficient of friction about x
        self.sigma_p = 0.35
        # Coefficient of friction about y
        self.sigma_y_rot = 0.44
        # Coefficient of friction about z
        self.sigma_r = 0.18
        # Coefficient of lateral resistance--> 0.6 for steel on hard ground
        self.mu = 0.6


class DC_wheel_motor():
    def __init__(self):
        # Viscous torque
        self.b = 0.008 #N*m
        # Moment of inertia of motor
        self.J_m = 0.005 #kg*m^2
        # Torque Constant
        self.K_t = 0.35 # Nm*A^-1
        # EMF Constant
        self.K_e = 0.35 #V rad^-1 s^-1
        # Inductance of Circuit
        self.L = 0.1 # H
        # Resistance in circuit
        self.R = 4 # Ohm
        # alpha
        self.alpha = -0.133 # A-1
        # Offset for efficiency curve
        self.gamma = 0.6
       # Base friction on Wheel
        self.eps = 0.002 #N*m*s*rad^-1
        """
        it may be assumed that motor efficiency is 0.7 nominally,
        gearbox efficiency is 0.6 nominally for planetary gears,
        and drive train efficiency is 0.7 nominally
        """



if __name__ == '__main__':
    # Initial parameters
    
    x_rover_v = np.array([0])
    y_rover_v = np.zeros(1)
    z_rover_v = np.zeros(1)
    phi_rover_v = np.zeros(1)
    theta_rover_v = np.zeros(1)
    psi_rover_v = np.array([np.deg2rad(30)])
    u_rover_v = np.zeros(1)
    v_rover_v = np.zeros(1)
    w_rover_v = np.zeros(1)
    p_rover_v = np.zeros(1)
    q_rover_v = np.zeros(1)
    r_rover_v = np.zeros(1)
    i_motor_1_v = np.zeros(1)
    i_motor_2_v = np.zeros(1)
    i_motor_3_v = np.zeros(1)
    i_motor_4_v = np.zeros(1)
    omega_motor_1_v = np.zeros(1)
    omega_motor_2_v = np.zeros(1)
    omega_motor_3_v = np.zeros(1)
    omega_motor_4_v = np.zeros(1)
    theta_motor_1_v = np.zeros(1)
    theta_motor_2_v = np.zeros(1)
    theta_motor_3_v = np.zeros(1)
    theta_motor_4_v = np.zeros(1)
    

    i_motor = np.array([i_motor_1_v[-1],i_motor_2_v[-1],i_motor_3_v[-1],i_motor_4_v[-1]])
    omega_motor = np.array([omega_motor_1_v[-1],omega_motor_2_v[-1],omega_motor_3_v[-1],omega_motor_4_v[-1]])
    
    # Time vector = np.arrange [s]
    h_step= 0.01 #data step [s]
    ti = 0 #initial time for integration [s]
    time = np.array([ti]) # time vector [s]
    
    y_init = np.array([x_rover_v[-1], y_rover_v[-1], z_rover_v[-1], 
                       phi_rover_v[-1], theta_rover_v[-1], psi_rover_v[-1], 
                       u_rover_v[-1], v_rover_v[-1], w_rover_v[-1], 
                       p_rover_v[-1], q_rover_v[-1], r_rover_v[-1],
                       i_motor_1_v[-1], i_motor_2_v[-1], i_motor_3_v[-1], i_motor_4_v[-1],
                       omega_motor_1_v[-1], omega_motor_2_v[-1],  omega_motor_3_v[-1], omega_motor_4_v[-1],
                       theta_motor_1_v[-1], theta_motor_2_v[-1],  theta_motor_3_v[-1], theta_motor_4_v[-1]])
    
    

    # Vector with the position goals are stored
    x_goal_v = np.array([3,4]) # [m]
    y_goal_v = np.array([5,0]) # [m]
    # Initial Goals [m]
    x_goal = x_goal_v[0]
    y_goal = y_goal_v[0]

    i=0
    exit_loop = 1


    V_motor = np.zeros(4)
    M_wheels = np.zeros(4)
    e_theta_v =[]
    
    v_target = 0.3 # Velocity we want to reach - target velocity
    Kp = 0.1 # Gain on the turn
    Kp_vel = 7.3 # Gain Voltage
    mu_s = 0.6 # longitudinal coeff of slip
    mu_gr = 0.1 #lateral/side coeff of slip
    
    while exit_loop == 1:
        
        
        Rover_properties= Rover_Properties()
        #  From Rover_Properties Class: --> All comments are in the relative class

        m = Rover_properties.mass #[kg]
        Ix = Rover_properties.Ix #[kg m^2]
        Iy = Rover_properties.Iy #[kg m^2]
        Iz = Rover_properties.Iz #[kg m^2]
        I = np.array([[Ix, 0, 0], [0,Iy,0], [0,0,Iz]]) #[kg m^2]
        R_wheel = Rover_properties.radius_wheel #[m]
        b = Rover_properties.b # body width
        l = Rover_properties.l  # body length
        d = np.sqrt(b**2+l**2) # distance between body center and wheel center
        
        #  Motor Proprieties
        motor_proprieties = DC_wheel_motor() 
        K_t = motor_proprieties.K_t #[Nm A-1]
        eff_motor = motor_proprieties.alpha*i_motor + motor_proprieties.gamma #[adim]
        L_motor = motor_proprieties.L #[H]
        R_motor = motor_proprieties.R #[Ohm]
        K_e = motor_proprieties.K_e  #[V rad^-1 s^-1]
        Jm_motor= motor_proprieties.J_m #[kg m^2]
        b_motor = motor_proprieties.b #[Nm]
        eps_motor = motor_proprieties.eps #[Nms rad^-1]
        

        # write the vector as a matrix and the put .T
        r_inertial = np.array([x_rover_v[-1],y_rover_v[-1],z_rover_v[-1]])
        #  Orientation in inertial reference system --> \map in ROS [rad]
        eta_inertial = np.array([phi_rover_v[-1], theta_rover_v[-1], psi_rover_v[-1]])
        # linear velocities in body reference system --> \base_footprint in ROS [m/s]
        v_body = np.array([u_rover_v[-1],v_rover_v[-1],w_rover_v[-1]])
        
        # EVALUATE THE VOLTAGE AT THE MOTOR
        # Heading angle between the actual and desired direction
        theta_target = np.arctan2((y_goal-y_rover_v[-1]),(x_goal-x_rover_v[-1]))
        # Error in heading between the actual and desired direction
        e_theta = theta_target - (psi_rover_v[-1])
        e_theta_v.append(e_theta) # just a vector to plot th error
        # Desired velocities of the wheels
        v_desired_left = v_target - Kp*e_theta
        v_desired_right = v_target + Kp*e_theta
        v_desired = np.array([v_desired_left,v_desired_left,v_desired_right,v_desired_right])
        
        
        
        # Voltage to get those desired velocities - Maximum voltage per motor 12 V
        for ii in range (0,4):
            V_motor[ii] = Kp_vel*(v_desired[ii]+(v_desired[ii]-R_wheel*omega_motor[ii]))
            V_motor[ii] = Kp_vel*(v_desired[ii]+(v_desired[ii]-R_wheel*omega_motor[ii]))
            if V_motor[ii] > 12:
                V_motor[ii] = 12
            if V_motor[ii] < 0:
                V_motor[ii] = 0 
        
        
        if i == 0:
            v_body_norm = np.array([np.linalg.norm(v_body)])
        else:
            v_body_norm =  np.append(v_body_norm, np.linalg.norm(v_body)) 

        # Angular velocities in body ref. frame [rad/s]
        omega_body = np.array([p_rover_v[-1], q_rover_v[-1], r_rover_v[-1]])

        #  F_FL = 0 ; F_BL = 1;  F_BR = 2; F_FR = 3
        F_prop_s = np.zeros(4) # Initialize force - Longitudinal Slip Force
        F_prop_g = np.zeros(4) # Initialize force - Rotation Frinction Force
        

        for ii in range(0,4):
            #  omega_motor is the rotational velocity
            F_prop_s[ii] = mu_s*(R_wheel*omega_motor[ii]-u_rover_v[-1])
            F_prop_g[ii] = mu_gr*d*(r_rover_v[-1])
        
        # Angle between the direction of the main movement and the lateral slip
        gamma = atan2(b,l)
        
        # Force and Moment acting on the overall body
        F_body = (F_prop_s.sum()+(F_prop_g[0]-F_prop_g[3]+F_prop_g[1]-F_prop_g[2])*np.cos(gamma))*np.array([1,0,0])
        M_body = d*((F_prop_s[3]+F_prop_s[2]-F_prop_s[1]-F_prop_s[0])*np.cos(gamma)-F_prop_g.sum())*np.array([0,0,1])
        # Moment Acting on the Wheels
        sign_wheels = np.array([1,1,-1,-1])
        for ii in range(0,4):
            #  omega_motor is the rotational velocity
            M_wheels[ii] = (K_t*i_motor[ii]-b_motor*omega_motor[ii]-eps_motor*omega_motor[ii]-R_wheel*F_prop_s[ii]+sign_wheels[ii]*R_wheel*F_prop_g[ii]*np.cos(gamma))

        

        if i == 0:
            M_prop_v = M_body[2]
            F_prop_v_x = F_body[0]
            F_prop_v_y= F_body[1]
            V_motor_l_v =  V_motor [0]
            V_motor_r_v = V_motor [2]
            # beta_v = np.array([beta])
        else:
            M_prop_v=np.append(M_prop_v,M_body[2])
            F_prop_v_x=np.append(F_prop_v_x,F_body[0])
            F_prop_v_y=np.append(F_prop_v_y,F_body[1])
            V_motor_l_v =np.append(V_motor_l_v, V_motor [0])
            V_motor_r_v =np.append(V_motor_r_v,V_motor [2])
            # beta_v = np.append(beta_v,(beta))  
            
        y_out=Utilities.rk4_integrator_one_step(Dynamics.Rover_Kinodynamics,h_step,y_init,ti,args=(F_body,M_body,M_wheels, I, m, 
                           L_motor, V_motor, R_motor, i_motor, K_e, omega_motor,Jm_motor, K_t,b_motor, eps_motor)) 
        
        # Inertial Position
        x_rover_v = np.append(x_rover_v, y_out [0])  
        y_rover_v =  np.append(y_rover_v, y_out [1])
        z_rover_v = np.append(z_rover_v, y_out [2])
        phi_rover_v = np.append(phi_rover_v, y_out [3])
        theta_rover_v = np.append(theta_rover_v, y_out [4])
        psi_rover_v = np.append(psi_rover_v, y_out [5])
        u_rover_v = np.append(u_rover_v, y_out [6])
        v_rover_v = np.append(v_rover_v, y_out [7])
        w_rover_v = np.append(w_rover_v, y_out [8])
        p_rover_v = np.append(p_rover_v, y_out [9])
        q_rover_v = np.append(q_rover_v, y_out [10])
        r_rover_v = np.append(r_rover_v, y_out [11])
        i_motor_1_v = np.append(i_motor_1_v, y_out [12])
        # if i_motor_1_v[-1] < 0:
        #     i_motor_1_v[-1] = 0
        i_motor_2_v = np.append(i_motor_2_v, y_out [13])
        # if i_motor_2_v[-1] < 0:
        #     i_motor_2_v[-1] = 0
        i_motor_3_v = np.append(i_motor_3_v, y_out [14])
        # if i_motor_3_v[-1] < 0:
        #     i_motor_3_v[-1] = 0
        i_motor_4_v = np.append(i_motor_4_v, y_out [15])
        # if i_motor_4_v[-1] < 0:
        #     i_motor_4_v[-1] = 0
        omega_motor_1_v = np.append(omega_motor_1_v, y_out [16])
        omega_motor_2_v = np.append(omega_motor_2_v, y_out [17])
        omega_motor_3_v = np.append(omega_motor_3_v, y_out [18])
        omega_motor_4_v = np.append(omega_motor_4_v, y_out [19])
        theta_motor_1_v = np.append(theta_motor_1_v, y_out [20])
        theta_motor_2_v = np.append(theta_motor_2_v, y_out [21])
        theta_motor_3_v = np.append(theta_motor_3_v, y_out [22])
        theta_motor_4_v = np.append(theta_motor_4_v, y_out [23])
        
        
        ti = ti+h_step
        time = np.append(time,ti)

        
        i_motor = np.array([i_motor_1_v[-1],i_motor_2_v[-1],i_motor_3_v[-1],i_motor_4_v[-1]])
        omega_motor = np.array([omega_motor_1_v[-1],omega_motor_2_v[-1],omega_motor_3_v[-1],omega_motor_4_v[-1]])
        
        y_init = y_out
        
        i = i+1


        
        if sqrt((x_rover_v[-1]-x_goal)**2+(y_rover_v[-1]-y_goal)**2)<10**-1:
            break

        if i == 2000:
            exit_loop = 2
            
    
    # PLOTS

    r_dot = np.diff(r_rover_v)/h_step
    v_dot = np.diff(u_rover_v)/h_step
    # Plots
    fig, ax = plt.subplots()
    ax.plot(x_rover_v, y_rover_v)
    ax.plot(x_goal, y_goal,'xr', label='XY')
    ax.legend()
    ax.set_ylabel('y [m]')
    ax.set_xlabel('x [m]')
    ax.grid(True)

    fig, ax = plt.subplots()
    ax.plot(time, x_rover_v)
    ax.set_ylabel('x [m/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True)

    fig, ax = plt.subplots()
    ax.plot(time, y_rover_v)
    ax.set_ylabel('y [m/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True)
    
    # Plots
    fig, ax = plt.subplots()
    ax.plot(time, u_rover_v)
    ax.set_ylabel('u [m/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True)
    # Plots
    fig, ax = plt.subplots()
    ax.plot(time, v_rover_v)
    ax.set_ylabel('v [m/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True)
    # # Plots
    # fig, ax = plt.subplots()
    # ax.plot(time, w_rover_v)
    # ax.set_ylabel('w [m/s]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True)
    # Plots
    # fig, ax = plt.subplots()
    # ax.plot(time,  np.rad2deg(phi_rover_v))
    # ax.set_ylabel('phi [m/s]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True)
    # # Plots
    # fig, ax = plt.subplots()
    # ax.plot(time,  np.rad2deg(theta_rover_v))
    # ax.set_ylabel('theta [m/s]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True)
    # Plots
    fig, ax = plt.subplots()
    ax.plot(time, np.rad2deg(psi_rover_v))
    ax.set_ylabel('psi [m/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True)       
    # Plots
    fig, ax = plt.subplots()
    ax.plot(time, i_motor_1_v,  label='1 motor')
    ax.plot(time, i_motor_2_v,  label='2 motor')
    ax.plot(time, i_motor_3_v,  label='3 motor')
    ax.plot(time, i_motor_4_v,  label='4 motor')
    ax.legend()
    ax.set_ylabel('i [A]')
    ax.set_xlabel('time [s]')
    ax.grid(True)       
    # fig.suptitle('psi', fontsize=16)    

    fig, ax = plt.subplots()
    ax.plot(time, theta_motor_1_v,  label='1 motor')
    ax.plot(time, theta_motor_2_v,  label='2 motor')
    ax.plot(time, theta_motor_3_v,  label='3 motor')
    ax.plot(time, theta_motor_4_v,  label='4 motor')
    ax.legend()
    ax.set_ylabel('Encoder Position [deg]')
    ax.set_xlabel('time [s]')
    ax.grid(True)   
    


    # Plots
    # fig, ax = plt.subplots()
    # ax.plot(np.linspace(0, ti, num=len(beta_v)), np.rad2deg(beta_v))
    # ax.set_ylabel('beta [deg]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True) 

    # # Plots
    # fig, ax = plt.subplots()
    # ax.plot(np.linspace(0, ti, num=len(v_body_norm)),v_body_norm)
    # ax.set_ylabel('velocity [m/s]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True) 

    # # Plots
    # fig, ax = plt.subplots()
    # ax.plot(time, np.rad2deg(q_rover_v))
    # ax.set_ylabel('q [rad/s]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True)  
    
    # # Plots
    # fig, ax = plt.subplots()
    # ax.plot(time, np.rad2deg(p_rover_v))
    # ax.set_ylabel('p [rad/s]')
    # ax.set_xlabel('time [s]')
    # ax.grid(True)  
    # Plots
    fig, ax = plt.subplots()
    ax.plot(time, np.rad2deg(r_rover_v))
    ax.set_ylabel('r [deg/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True) 
    # Plots
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, ti, num=len(r_dot)), np.rad2deg(r_dot))
    ax.set_ylabel('r_dot [deg/ss]')
    ax.set_xlabel('time [s]')
    ax.grid(True)  
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, ti, num=len(v_dot)),v_dot)
    ax.set_ylabel('v_dot [m/ss]')
    ax.set_xlabel('time [s]')
    ax.grid(True) 
    # Plots
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, ti, num=len(v_body_norm)), M_prop_v)
    ax.set_ylabel('M_prop [Nm]')
    ax.set_xlabel('time [s]')
    ax.grid(True) 
    
    # Plots
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, ti, num=len(v_body_norm)), F_prop_v_x)
    ax.set_ylabel('Fx_prop [N]')
    ax.set_xlabel('time [s]')
    ax.grid(True) 
    
    # Plots
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, ti, num=len(v_body_norm)),F_prop_v_y)
    ax.set_ylabel('Fy_prop [N]')
    ax.set_xlabel('time [s]')
    ax.grid(True) 
    
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, ti, num=len(V_motor_l_v)), V_motor_l_v ,  label='Voltage left')
    ax.plot(np.linspace(0, ti, num=len(V_motor_r_v)), V_motor_r_v ,  label='Voltage right')
    ax.legend()
    ax.set_ylabel('Voltage [V]')
    ax.set_xlabel('time [s]')
    ax.grid(True)  
    
    e_theta_v
    fig, ax = plt.subplots()
    ax.plot(time[1::], np.rad2deg(e_theta_v))
    ax.set_ylabel('error in heading[deg/s]')
    ax.set_xlabel('time [s]')
    ax.grid(True) 