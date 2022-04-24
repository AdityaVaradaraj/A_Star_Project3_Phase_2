<h1>Project 3 - Implementation of AStar Algorithm for a rigid robot with Dublin Curves in ROS!</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. Install ROS

Note:  Other libraries used are inbuilt.</br>

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/SamPusegaonkar/ENPM661
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd ENPM661/Project3/Part2'
    4. To Run AStar, Navigate to 'cd Phase 2'. If OS is Ubuntu, type 'python3 AStar.py'
    5. Enter the parameters of the  robot
    6. Enjoy!


<h1>Videos are present in the 'Output Videos' folder. The output can also be viewed below in GIF format.</h2>

<h1> r = 0.105, Clerance = 0.2 </h1>

<h2> Test Case 1: Starting Coordinate = (1, 1, 0), Ending Coordinate = (9, 9) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/116009416-860d9e80-a5e7-11eb-8965-4f7c2775f2d4.gif" alt="Logo"/>
</p>

<h2> Test Case 2: Starting Coordinate = (8, 5, 0), Ending Coordinate = (7, 7) </h2>

<p align="center">
  
  <img src="https://user-images.githubusercontent.com/12711480/116009414-860d9e80-a5e7-11eb-9ff5-97670a9dab58.gif" alt="Logo"/>
</p>
 <h2> Test Case 3: Starting Coordinate = (6, 8, 0), Ending Coordinate = (9, 9) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/116009415-860d9e80-a5e7-11eb-8044-d994e4fc596f.gif" alt="Logo"/>
</p>




## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the distance to reach that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle or outside the arena
  5. All the equations for the algebraic planes are defined in their approppriate methods.