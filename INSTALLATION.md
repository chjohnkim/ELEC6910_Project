
## VREP_ROS Simulation Environment Instruction
This is a method to setup V-REP in ROS Envronment. 


## Envrironment
This setup was tested with the following versions: 
[ROS: Kinetic](http://wiki.ros.org/kinetic)
[V-REP: 3.5.0 PRO EDU](http://coppeliarobotics.com/files/V-REP_PRO_EDU_V3_5_0_Linux.tar.gz)
Plugins(Please git clone them from the latest master):
[vrep_ros_bridge](https://github.com/lagadic/vrep_ros_bridge)
[vrep_ros_interface](https://github.com/CoppeliaRobotics/v_repExtRosInterface)
Platform: Ubuntu 16.04 LTS


## Tutorial
Here are some useful links:
[Ros Bridge Installation test](http://wiki.ros.org/vrep_ros_bridge#Installation_test)
Note: Since installation of vrep_ros_bridge uses catkin_make, and ROS Interface plugin for V-REP uses catkin build, you can create different catkin workspaces for them, refer to this article 
[Create a temporary catkin workspace for ROS Interface](http://analuciacruz.me/articles/RosInterface_kinetic/).


## V-REP Installation
1. Download the VREP installation file
[V-REP: 3.5.0 PRO EDU](http://www.coppeliarobotics.com/downloads.html)
2. Extract to a folder of your choice. (Preferably in /home/software)
3. In Terminal, go to the root of your vrep folder and run the software to see whether installation worked correctly. 
>> cd ~/vrep
>> ./vrep.sh 


## V-Rep Ros Bridge Plugin Installation
[V-Rep ROS Bridge](https://github.com/lagadic/vrep_ros_bridge)
1. Go in the src folder of your catkin workspace in catkin_ws/src via terminal
2. Download the plugin from GIT typing:
>> git clone https://github.com/lagadic/vrep_ros_bridge.git
3. Go in the quadrotor_tk_handler sub-folder via terminal
>> cd catkin_ws/src/vrep_ros_bridge/quadrotor_tk_handler
>> touch CATKIN_IGNORE
4. Open the file bashrc: 
>> gedit ~/.bashrc
5. In the end of the bash file add:
>> export VREP_ROOT_DIR=/ChangeWithyourPathToVrep/
>> export VREP_ROOT=/ChangeWithyourPathToVrep/
>> export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:/ChangeWithYour_path_to_catkin_ws/catkin_ws/src
>> source /opt/ros/kinetic/setup.bash
>> source /ChangeWithYour_path_to_catkin_ws/catkin_ws/devel/setup.bash
-Note: This part may need debugging. Try cd-ing and echo-ing to the VREP_ROOT until it works
6. Go in your catkin_ws and run:
>> catkin_make
7. Now build again the pkg using the next instruction:
>> catkin_make --pkg vrep_ros_bridge --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
8. In the folder catkin_ws/devel/lib/ you will find the main library (libv_repExtRosBridge.so) and the others libraries (libcamera_handler.so, libmanipulator_handler.so, libquadrotor_handler.so, librigid_body_handler.so ).
9. The file libv_repExtRosBridge.so has to be in the V-Rep installation folder in order to be loaded. What we will do is to create a symbolic link to it. Go via terminal to the installation folder of V-Rep and type:
>> ln -s /YOUR_CATKIN_WS_PATH/devel/lib/libv_repExtRosBridge.so
10. If you are using Ubuntu 16.04 and ROS Kinetic you will need to compile the plugin by yourself: Copy the folders vrep_plugin and vrep_common from home/user/Desktop/V-REP_PRO_V3_3_2_64_Linux/programming/ros_packages in your catkin_ws/src and do a catkin_make. You will find in devel the file libv_repExtRos.so. You will need to copy it in the root of the new V-REP Folder.
-Note: You need to download [V-REP_PRO_V3_3_2_64_Linux]
11. In order to test if the installation was successful, go to: [vrep_ros_bridge Wiki](http://wiki.ros.org/vrep_ros_bridge#Installation_test)



## ROS Interface Plugin for V-REP Installation 
[vrep_ros_interface](https://github.com/CoppeliaRobotics/v_repExtRosInterface)
[Create a temporary catkin workspace for ROS Interface](http://analuciacruz.me/articles/RosInterface_kinetic/)
1. Install ROS kinetic and the V-REP Stubs generator’s required software
>> sudo apt-get install -y ros-kinetic-desktop-full git cmake python-tempita python-catkin-tools python-lxml
2. Clone the V-REP Stubs generator. Clone this repository in the directory of your choice.
>> git clone -q https://github.com/fferri/v_repStubsGen.git
3. Add its path to the search path for importing python modules
>> export PYTHONPATH=$PYTHONPATH:$PWD
4. Clone & build the RosInterface in your catkin_ws
>> cd catkin_ws/src
>> git clone --recursive https://github.com/CoppeliaRobotics/v_repExtRosInterface.git vrep_ros_interface
5. Next, build the workspace:
>> catkin build
6. Check that the resulting vrep-ros library is in the devel folder
>> cd ../devel/lib/
>> ls
7. Source the workspace
8. Copy the library in your V-REP installation folder. 
devel/lib/libv_repExtRosInterface.so > cp > VREP_ROOT


## Some things to keep in mind during instllation: 
1. The export VREP_ROOT may need to be debugged in the .bashrc file. Try cd-ing and echo-ing to the VREP_ROOT until it works.  
>> export VREP_ROOT=/ChangeWithyourPathToVrep/
2. There is a total of three library files that needs to be copied to the vrep root folder. 
libv_repExtRos.so (from compiling V-REP_PRO_V3_3_2_64_linux)
repExtRosBridge.so (from compiling V-Rep ROS Bridge)
libv_repExtRosInterface.so (from compiling ROS Interface Plugin) 
3. Some other softwares may need to be installed during the process such as: 
[OpenCV]
>> sudo apt-get install libopencv-dev python-opencv
[Eigen3]
>> sudo apt install libeigen3-dev

