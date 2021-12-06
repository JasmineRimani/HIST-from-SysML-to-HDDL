# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 14:29:45 2021

@author: jasmi
"""

import numpy as np
from scipy.spatial.transform import Rotation as R
from math import atan2, sqrt, floor, ceil
import matplotlib.pyplot as plt
from Utilities import Utilities 
import pandas as pd
from datetime import datetime, timedelta
import calendar, time
from scipy.spatial.transform import Rotation as R

class Process_Excel():
    def __init__(self, file_pose, file_cmd_vel, file_joint_state, set_time_interval):
        self.file_pose = file_pose
        self.file_cmd_vel = file_cmd_vel
        self.file_joint_state = file_joint_state
        self.set_time_interval = set_time_interval
    
    def date_converter(self, time):
        time_coverted = []
        
        
        if hasattr(time[0], 'item') and type(time[0].item()) is int: 

            initial_time = time[0]
                                                     
            for xx in time:
                time_coverted.append((xx-initial_time))
            
        
        if type(time[0]) is str:

            time_vector = time[0].split('/')[-1].split(':')
            time_vector_init = [float(x) for x in time_vector]
            initial_day = time_vector_init[0]
            initial_time = time_vector_init[1]*60+time_vector_init[2]
            
            for xx in time:
                xx_vector_init = xx.split('/')[-1].split(':')
                xx_vector = [float(yy) for yy in xx_vector_init]
                day = xx_vector[0]
                time_xx = xx_vector[1]*60+xx_vector[2]
                
                diff_day = (day-initial_day)*60*60*24
                
                time_coverted.append((time_xx-initial_time)+diff_day)
            
        return [x for x in time_coverted]    

    def get_index(self, vector):
            index_needed = len(vector)-1
            for index, yy in enumerate(vector):
                if floor(yy) == self.set_time_interval:
                    index_needed = index
                if ceil(yy) == self.set_time_interval:
                    index_needed = index
            
            return index_needed

    
    def read_excel(self):
        
        # Get the Pose
        df = pd.read_csv(self.file_pose)
        # print(df)
        time_pose = df[".header.stamp.secs"]
        time_processed_pose = self.date_converter(time_pose)
        x = 0
        position_x = df[".pose.position.x"]
        position_y = df[".pose.position.y"]
        rotation_x = df[".pose.orientation.x"]
        rotation_y = df[".pose.orientation.y"]
        rotation_z = df[".pose.orientation.z"]
        rotation_w = df[".pose.orientation.w"]
        
        rotation_x_eul = []
        rotation_y_eul = []
        rotation_z_eul = []
        
        for x_init, y_init, z_init, w_init in zip(rotation_x, rotation_y, rotation_z, rotation_w):
            x_eul, y_eul, z_eul = Utilities.quaternion_to_euler(x_init, y_init, z_init, w_init)
            rotation_x_eul.append(x_eul) 
            rotation_y_eul.append(y_eul) 
            rotation_z_eul.append(z_eul)
        
        
        index = self.get_index(time_processed_pose)
        
        time_processed_pose = time_processed_pose[0:index]
        position_x = position_x[0:index]
        position_y = position_y[0:index]
        rotation_z_eul = rotation_z_eul[0:index]
        
        
        
        # Get the commanded velocity
        df = pd.read_csv(self.file_cmd_vel)
        # Get your data!
        time_cmd_vel = df["time"] 
        time_processed_cmd_vel = self.date_converter(time_cmd_vel)
        cmd_vel_x = df[".linear.x"] 
        cmd_vel_yaw = df[".angular.z"]
        
        index = self.get_index(time_processed_cmd_vel)
        time_processed_cmd_vel = time_processed_cmd_vel[0:index]
        cmd_vel_x = cmd_vel_x[0:index]
        cmd_vel_yaw = cmd_vel_yaw[0:index]
        
        # Get your data!
        df = pd.read_csv(self.file_joint_state)
        time_joint_state = df["time"] 
        time_processed_joint_state = self.date_converter(time_joint_state)
        
        joint_position = df[".position"] 
        joint_velocity = df[".velocity"] 
        joint_effort = df[".effort"] 
        FL_joint_effort = []
        FL_joint_position = []
        FL_joint_velocity = []
        FR_joint_effort = []
        FR_joint_position = []
        FR_joint_velocity = []
        RL_joint_effort = []
        RL_joint_position = []
        RL_joint_velocity = []
        RR_joint_effort = []
        RR_joint_position = []
        RR_joint_velocity = []
        
        for position_init, velocity_init, effort_init in zip(joint_position, joint_velocity, joint_effort):
            position_vect = position_init.replace(')','').replace('(','').split(',')
            position = [float(x) for x in position_vect]
            velocity_vect = velocity_init.replace(')','').replace('(','').split(',')
            velocity = [float(x) for x in velocity_vect]
            effort_vect = effort_init.replace(')','').replace('(','').split(',')
            effort = [float(x) for x in effort_vect]
            
            FL_joint_effort.append(effort[0])
            FL_joint_position.append(position[0])
            FL_joint_velocity.append(velocity[0])
            FR_joint_effort.append(effort[1])
            FR_joint_position.append(position[1])
            FR_joint_velocity.append(velocity[1])
            RL_joint_effort.append(effort[2])
            RL_joint_position.append(position[2])
            RL_joint_velocity.append(velocity[2])
            RR_joint_effort.append(effort[3])
            RR_joint_position.append(position[3])
            RR_joint_velocity.append(velocity[3])            
        
        index = self.get_index(time_processed_joint_state)
        time_processed_joint_state = time_processed_joint_state[0:index]
        FL_joint_effort = FL_joint_effort[0:index]
        FL_joint_position = FL_joint_position[0:index]
        FL_joint_velocity = FL_joint_velocity[0:index]
        FR_joint_effort = FR_joint_effort[0:index]
        FR_joint_position = FR_joint_position[0:index]
        FR_joint_velocity = FR_joint_velocity[0:index] 
        RL_joint_effort = RL_joint_effort[0:index]
        RL_joint_position = RL_joint_position[0:index]
        RL_joint_velocity = RL_joint_velocity[0:index]
        RR_joint_effort = RR_joint_effort[0:index]
        RR_joint_position = RR_joint_position[0:index]
        RR_joint_velocity = RR_joint_velocity[0:index]   
        
        # plot the variables
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_pose, position_x,  label='x pose of the rover')
        # ax.set_ylabel('Position of the Rover along x (map reference system) [m]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_pose, position_y,  label='y pose of the rover')
        # ax.set_ylabel('Position of the Rover along y (map reference system) [m]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)

        # fig, ax = plt.subplots()
        # ax.plot(time_processed_pose, [ x*180/np.pi for x in rotation_z_eul],  label='rotation along z of the rover')
        # ax.set_ylabel('rotation along z of the rover (map reference system) [deg]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(position_x, position_y)
        # ax.set_ylabel('Position of the Rover along y (map reference system) [m]')
        # ax.set_xlabel('Position of the Rover along x (map reference system) [m]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_cmd_vel, cmd_vel_x)
        # ax.set_ylabel('Cmd vel in x [m/s]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
            
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_cmd_vel, cmd_vel_yaw)
        # ax.set_ylabel('Cmd rotational velocity [rad/s]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, FL_joint_effort)
        # ax.set_ylabel('FL_joint_effort [Nm]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, FR_joint_effort)
        # ax.set_ylabel('FR_joint_effort [Nm]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, RL_joint_effort)
        # ax.set_ylabel('RL_joint_effort [Nm]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, RR_joint_effort)
        # ax.set_ylabel('RR_joint_effort [Nm]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, FL_joint_position)
        # ax.set_ylabel('FL_joint_position [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, FR_joint_position)
        # ax.set_ylabel('FR_joint_position [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, RL_joint_position)
        # ax.set_ylabel('RL_joint_position [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, RR_joint_position)
        # ax.set_ylabel('RR_joint_position [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)

        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, FL_joint_velocity)
        # ax.set_ylabel('FL_joint_velocity [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, FR_joint_velocity)
        # ax.set_ylabel('FR_joint_velocity [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, RL_joint_velocity)
        # ax.set_ylabel('RL_joint_velocity [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)
        
        # fig, ax = plt.subplots()
        # ax.plot(time_processed_joint_state, RR_joint_velocity)
        # ax.set_ylabel('RR_joint_velocity [rad]')
        # ax.set_xlabel('time [s]')
        # ax.grid(True)        

        
        return time_processed_pose, position_x, position_y, rotation_z_eul, \
               time_processed_cmd_vel, cmd_vel_x, cmd_vel_yaw, time_processed_joint_state, FL_joint_effort, FR_joint_effort, RL_joint_effort,\
               RR_joint_effort, FL_joint_position, FR_joint_position, RL_joint_position, RR_joint_position,\
               FL_joint_velocity, FR_joint_velocity, RL_joint_velocity, RR_joint_velocity
               
    
    
    
def main():
    file_pose = 'bagfile-vrpn_client_node-LeoRover-pose.csv '
    file_cmd_vel = 'bagfile-cmd_vel.csv '
    file_joint_state = 'bagfile-joint_states.csv'
    set_time_interval = 45 #[s]
    dummy_class = Process_Excel(file_pose, file_cmd_vel, file_joint_state, set_time_interval)
    time_processed_pose, position_x, position_y, rotation_z_eul, \
               time_processed_cmd_vel, cmd_vel_x, cmd_vel_yaw, time_processed_joint_state, FL_joint_effort, FR_joint_effort, RL_joint_effort,\
               RL_joint_effort, FL_joint_position, FR_joint_position, RL_joint_position, RR_joint_position,\
               FL_joint_velocity, FR_joint_velocity, RL_joint_velocity, RR_joint_velocity = dummy_class.read_excel()


if __name__ == "__main__":
    main()
    
    
        