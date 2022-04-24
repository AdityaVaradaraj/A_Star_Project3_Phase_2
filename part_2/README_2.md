## Project 3 Phase 2 Part 2: Gazebo
##### Project Group:
###### Aditya Varadaraj 117054859
###### Saurabh Palande 118133959

##### Requirements:
rospy
math
heapq
std_msgs
geometry_msgs

##### Instructions:
1) Unzip the folder. Copy paste the content of astar_proj3 package in part_2 folder into a package named astar_proj3 in the src of your catkin workspace and 
```
catkin_make
```
or 
```
catkin build 
```
and 
```
source devel/setup.bash
```
2) Export turtlebot3 burger model
3) In one terminal, run:
```
roslaunch astar_proj3 turtlebot3_map.launch x_pos:=-4 y_pos:=-4 z_pos:=0
```
4) Adjust view
5) In another terminal, navigate inside the src of the package and run:
```
python3 publisher.py
```
6) Enter start coordinates x=1, y=1, theta=0 when prompted
7) Enter goal x=9, y=9
8) Enter RPM1 = 10, RPM2 = 15
9) Enter radius of robot = 0.105 (We use Burger here)
10) Enter the cl (clearance)= 0.3
