# JUST THE LOG OF THE TEST PERFORMED
-----------------------------------------------------------------------------------------------------------
**Sensor Launch + static tf + throttles**
roslaunch my_pcl_tutorial rover_sensors.launch

-----------------------------------------------------------------------------------------------------------

**Hector Mapping - to create a map of the environment**
roslaunch hector_mapping mapping_default.launch odom_frame:=T265_odom_frame base_frame:=base_link
**Control the system remotely**
rosrun leo_navigation teleop.py
**Save Map**
rosrun map_server map_saver -f last_map (after -f put name of the file you want the map to be saved to)


-----------------------------------------------------------------------------------------------------------
**amcl - test1: pure amcl withe T265_odom_frame. Doesn't like to much turning fast in the same spot.**

-----------------------------------------------------------------------------------------------------------
**amcl2_hector_mapping localization:**
- first: roslaunch leo_navigation hector.launch 
- second: roslaunch leo_navigation amcl_hector.launch 
- problem - you have to erase the link between T265 odom sample and base_link- so that you can have a link between scan odom and base link
*Commented that link in rover_sensor and created a new launch file rover_sensor_hector.launch
Worst localization than amcl - not usable!!!!!*

**amcl - test3 - fake_localization - same results of amcl - we stay on the amcl**

-----------------------------------------------------------------------------------------------------------
**Move_base test 1 - leo_rover_parameters in the husky planner**
- launch sensors: roslaunch my_pcl_tutorial rover_sensors.launch
- launch amcl:  roslaunch leo_navigation amcl.launch (or fake_localization)
- launch move_base: roslaunch leo_navigation move_base.launch

can the system avoid obstacles? Yep
can it free itself?
can it find paths to move? Yep

It works with a good map it should be able to move.
**However the planner is not following the right trajectory**

---------------------------------------------------------------------------------------------------------------
**Move_base test 2 - asr_navf** <-- This works like a charm!!!!
asr_navf --> gloabal planner --> new package in igluna_ws/src
*folder: igluna_ws/src/nav_asr* 
```
root@leodroid:~/igluna_ws/src/nav_asr# ls
asr_ftc_local_planner  asr_navfn  navigation
root@leodroid:~/igluna_ws/src/nav_asr# cd asr_ftc_local_planner/
root@leodroid:~/igluna_ws/src/nav_asr/asr_ftc_local_planner# ls
CMakeLists.txt  README.md       cfg      package.xml
License.txt     blp_plugin.xml  include  src
root@leodroid:~/igluna_ws/src/nav_asr/asr_ftc_local_planner# cd cfg/
root@leodroid:~/igluna_ws/src/nav_asr/asr_ftc_local_planner/cfg# ls
FTCPlanner.cfg

```

**Changed**: (indeed it doesn't change that much)
- BaseLocalPlanner.cfg in ~/igluna_ws/src/nav_asr/navigation/base_local_planner/cfg 
   - From: gen.add("holonomic_robot", bool_t, 0, "Set this to true if the robot being controlled can take y velocities and false otherwise",True)
   - To: gen.add("holonomic_robot", bool_t, 0, "Set this to true if the robot being controlled can take y velocities and false otherwise",False)


* Change Parameters*: navigation --> base_local_planner move_base / cost_map

New Test:
**Test new navigation stack --> it works!!!!!**
Launch:
1 roslaunch my_pcl_tutorial rover_sensors.launch
2 amcl or fake localization
3 roslaunch leo_navigation move_base_asr_navf.launch 

**Move base without the map** --> or you can directly explore the environment with the keyboard control (if you are not able to test this!!) --> this work!!!
1 roslaunch my_pcl_tutorial rover_sensors.launch
2 roslaunch hector_mapping mapping_default.launch odom_frame:=T265_odom_frame base_frame:=base_link
3 roslaunch leo_navigation move_base_asr_navf.launch 

**Test the mapping buddle that Maximilien created for the rover** --> NOT DONE
- rosrun my_pcl_tutorial pointcloud_saver_server
- roslaunch my_pcl_tutorial dronemappingphase.launch filename_tag:=/root/database/dronedatabase.txt
- rosrun my_pcl_tutorial pointcloud_saver_client /octomap_point_cloud_centers /root/database/ '3DdemMap.pcd'

**Test the Drone Mapping** 
1 roslaunch state_machine startdrone.launch
2 rosrun state_machine MappingStateMachine.py  --> change the dimension of the exploration area!!!
3 rosbag record -o test_drone_ /vrpn_client_node/Quadri_MK_4/pose /tf /tf_static /mavros/vision_pose/pose /mavros/state /mavros/setpoint_position/local /mavros/local_position/pose /mavros/local_position/velocity_local /T265/odom/sample /D435/depth/color/points /D435/color/image_raw/compressed /D435/color/camera_info  /octomap_point_cloud_centers /occupied_cells_vis_array /ar_pose_marker /visualization_marker



-----------------------------------------------------------------------------------------------------------------------------------------------



**Topic to register**
no move base:

rosbag record /tf /tf_static /cmd_vel /joint_states /T265/odom/sample /vrpn_client_node/LeoRover/pose /battery


with move base:

rosbag record /tf /tf_static /cmd_vel /joint_states /T265/odom/sample /vrpn_client_node/LeoRover/pose /battery /map /amcl_pose /move_base/GlobalPlanner/parameter_descriptions/move_base/GlobalPlanner/parameter_updates /move_base/GlobalPlanner/plan /move_base/GlobalPlanner/potential /move_base/TrajectoryPlannerROS/cost_cloud /move_base/TrajectoryPlannerROS/global_plan /move_base/TrajectoryPlannerROS/local_plan /move_base/TrajectoryPlannerROS/parameter_descriptions /move_base/TrajectoryPlannerROS/parameter_updates /move_base/cancel /move_base/current_goal /move_base/feedback /move_base/global_costmap/costmap /move_base/global_costmap/costmap_updates /move_base/global_costmap/footprint /move_base/global_costmap/inflation_layer/parameter_descriptions /move_base/global_costmap/inflation_layer/parameter_updates /move_base/global_costmap/obstacle_layer/parameter_descriptions /move_base/global_costmap/obstacle_layer/parameter_updates /move_base/global_costmap/parameter_descriptions /move_base/global_costmap/parameter_updates/move_base/global_costmap/static_layer/parameter_descriptions /move_base/global_costmap/static_layer/parameter_updates /move_base/goal /move_base/local_costmap/costmap/move_base/local_costmap/costmap_updates /move_base/local_costmap/footprint /move_base/local_costmap/inflation_layer/parameter_descriptions /move_base/local_costmap/inflation_layer/parameter_updates /move_base/local_costmap/obstacle_layer/parameter_descriptions /move_base/local_costmap/obstacle_layer/parameter_updates /move_base/local_costmap/parameter_descriptions /move_base/local_costmap/parameter_updates /move_base/parameter_descriptions /move_base/parameter_updates /move_base/result /move_base/status /move_base_simple/goal





**isae network problems fixing**
export http_proxy=http://proxy.isae.fr:3128 --> isae network
sudo -E apt update (-E maintains the environment variables)
sudo -E  apt install ros-melodic-joy (-E maintains the environment variables, so you don't loose your export)

--------------------------------------------------------------------------------------------------------------------------------------------

**To Save**
Save the rosbags (simple movement and movebase)
Save the rqt_graph and trees

---------------------------------------------------------------------------------------------------------------------------------------------

**To install on the rover new packages:**
- export proxy (the http address is the one linked to the computer connected to the rover):
- root@leodroid:~# export https_proxy=http://10.255.100.224:3128
- Set up your keys: (http://wiki.ros.org/melodic/Installation/Ubuntu) --> after a bit the keys on the keys of the system can become obsolete and we may be in need to update them
- root@leodroid:~# curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
**Update the ros packages:**
- root@leodroid:~# apt update
**Install what you need:**

------------------------------------------------------------------------------------------------------------------------------------------------
**Recover Bags**
recover bag - scp root@10.255.110.2:/root/*.bag Bureau/test_07_12_2021/

------------------------------------------------------------------------------------------------------------------------------------------------
**New package to the src REMEMBER TO COMPILE THE WORKSPACE!!! (catkin_make or catkin build)**



