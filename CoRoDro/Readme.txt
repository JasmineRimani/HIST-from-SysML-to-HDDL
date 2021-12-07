Sensor Launch + static tf + throttles
roslaunch my_pcl_tutorial rover_sensors.launch

Hector Mapping - to create a map of the environment
roslaunch hector_mapping mapping_default.launch odom_frame:=T265_odom_frame base_frame:=base_link
Save Map
roslaunch map_server map_saver




Topic to register
rosbag record /tf /tf_static /cmd_vel /joint_states /T265/odom/sample /vrpn_client_node/LeoRover/pose /battery



isae network problems
export http_proxy=http://proxy.isae.fr:3128 --> isae network
sudo -E apt update (-E maintains the environment variables)
sudo -E  apt install ros-melodic-joy (-E maintains the environment variables, so you don't loose your export)

