import pygame
import math
import heapq
import time


h = 500
w = 500
white = (255, 255, 255)
blue = (0,0, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)


class Node:

    def __init__(self, x, y, endX, endY, theta):
        self.i = x
        self.j = y
        self.theta = theta
        self.costToCome = 0.0
        self.costToGo = 2.5*(math.sqrt((x - endX) ** 2 + (y - endY) ** 2))
        self.cost = None
        self.neighbours = {}
        self.valid_actions = {}
        self.parent = None

    def __lt__(self, other):
        return self.cost < other.cost


class Graph:

    def __init__(self, start, end, RPM1, RPM2, radius, cl):
        self.visited = {}
        self.endX = end.i
        self.endY = end.j
        self.RPM1 = RPM1
        self.RPM2 = RPM2
        self.radius = radius
        self.cl = cl + self.radius

    def new_coords(self, i, j, theta, UL, UR):
        t = 0
        r = 0.22
        L = 0.287
        dt = 0.1

        UL = 3.14*UL/30
        UR = 3.14*UR/30

        newX = i
        newY = j
        newTheta = 3.14 * theta/180
        D = 0

        while t < 1:
            t = t + dt
            Delta_Xn = 0.5 * r * (UL + UR) * math.cos(newTheta) * dt
            Delta_Yn = 0.5 * r * (UL + UR) * math.sin(newTheta) * dt
            newX += Delta_Xn
            newY += Delta_Yn
            newTheta += (r / L) * (UR - UL) * dt
            D = D + math.sqrt(math.pow(Delta_Xn, 2) + math.pow(Delta_Yn, 2))
        newTheta = 180*newTheta/3.14

        if newTheta > 0:
            newTheta = newTheta % 360
        elif newTheta < 0:
            newTheta = (newTheta + 360) % 360

        newX = self.round_num(newX)
        newY = self.round_num(newY)

        return newX, newY, newTheta, D
    def neighbours(self, currentNode):
        i, j, theta = currentNode.i, currentNode.j, currentNode.theta
        neighbours = {}
        valid_actions = {}
        actions = [[0, self.RPM1], [self.RPM1, 0], [self.RPM1, self.RPM1], [0, self.RPM2], [self.RPM2, 0], [self.RPM2, self.RPM2], [self.RPM1, self.RPM2], [self.RPM2, self.RPM1]]
        for UL, UR in actions:
            x, y, newTheta, distance = self.new_coords(i, j, theta, UL, UR)
            if (not self.isOutsideArena(x, y)) and (not self.isAnObstacle(x, y)):
                newNode = Node(x, y, self.endX, self.endY, newTheta)
                neighbours[newNode] = distance
                valid_actions[newNode] = [UL, UR]
        return neighbours, valid_actions

    

    def drawActionSet(self, x, y, theta, UL, UR, color):
        t = 0
        r = 0.22
        L = 0.287
        dt = 0.1

        newX = x
        newY = y
        newTheta = 3.14*theta/180
        UL = 3.14*UL/30
        UR = 3.14*UR/30

        while t < 1:
            t = t + dt
            oldX = newX
            oldY = newY
            newX += 0.5 * r * (UL + UR) * math.cos(newTheta) * dt
            newY += 0.5 * r * (UL + UR) * math.sin(newTheta) * dt
            pygame.draw.line(gridDisplay, color, [int(50*oldX), int(h - 50*oldY)], [int(50*newX), int(h - 50*newY)], 2)
            newTheta += (r / L) * (UR - UL) * dt
        pygame.display.update()
        time.sleep(0.1)

        return


    def round_num(self, i):

        i = 50*i
        i = int(i)
        i = i/50
        return i

    def generateGraph(self):
        gridDisplay.fill(white)
        pygame.draw.circle(gridDisplay, black, [100, int(h - 100)], 50)
        pygame.draw.circle(gridDisplay, black, [100, int(h - 400)], 50)
        pygame.draw.polygon(gridDisplay, black, [(int(50*0.25), int(h - 50*5.75)), (int(50*1.75), int(h - 50*5.75)), (int(50*1.75), int(h - 50*4.25)), (50*0.25, h - 50*4.25)])
        pygame.draw.polygon(gridDisplay, black, [(int(50*3.75), int(h - 50*5.75)), (int(50*6.25), int(h - 50*5.75)), (int(50*6.25), int(h) - int(50*4.25)), (int(50*3.75), int(h - 50*4.25))])
        pygame.draw.polygon(gridDisplay, black, [(int(50*7.25), int(h - 50*4)), (int(50*8.75), int(h - 50*4)), (int(50*8.75), int(h - 50*2)), (int(50*7.25), int(h - 50*2))])

    def performAStar(self, start, end):
        if self.isAnObstacle(start.i, start.j) and self.isAnObstacle(end.i, end.j):
            print("Starting and endXng point are inside the obstacle!")
            return

        if self.isAnObstacle(start.i, start.j):
            print("Starting point is inside the obstacle!")
            return
        if self.isAnObstacle(end.i, end.j):
            print("EndXng point is inside the obstacle!")
            return

        if self.isOutsideArena(start.i, start.j):
            print("Starting point is outside the arena!")
            return

        if self.isOutsideArena(end.i, end.j):
            print("EndXng point is outside the arena!")
            return

        print("Started A-star algorithm")
        priorityQueue = []
        visited_list = {}
        heapq.heappush(priorityQueue, (start.cost, start))
        while len(priorityQueue):
            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]
            if self.isInTargetArea(currentNode.i, currentNode.j):
                print("Found a path!")
                return True

            if tuple([currentNode.i, currentNode.j]) in visited_list:
                continue
            visited_list[tuple([currentNode.i, currentNode.j])] = True

            currentDistance = currentNode.costToCome
            neighbours, valid_actions = self.neighbours(currentNode)
            currentNode.neighbours = neighbours
            currentNode.valid_actions = valid_actions
            for neighbourNode, newDistance in neighbours.items():
                neighbourNode.costToCome = currentDistance + newDistance
                neighbourNode.cost = neighbourNode.costToCome + neighbourNode.costToGo
                neighbourNode.parent = currentNode
                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))
                print((neighbourNode.i, neighbourNode.j))
        print("No path found")
        return False

    def visualize(self, start, end):

        visited_list = {}
        priorityQueue = []
        heapq.heappush(priorityQueue, (start.cost, start))
        pygame.draw.circle(gridDisplay, black, [int(50*start.i), int(h - 50*start.j)], 5)
        pygame.draw.circle(gridDisplay, black, [int(50*end.i), int(h - 50*end.j)], 5)
        pygame.display.update()
        while len(priorityQueue):

            currentNode = heapq.heappop(priorityQueue)
            currentNode = currentNode[1]

            if self.isInTargetArea(currentNode.i, currentNode.j):
                self.backTrack(currentNode)
                print("Total distance from start to goal is:", currentNode.costToCome)
                return

            if tuple([currentNode.i, currentNode.j]) in visited_list:
                continue
            visited_list[tuple([currentNode.i, currentNode.j])] = True

            for neighbourNode, action in currentNode.valid_actions.items():
                self.drawActionSet(currentNode.i,currentNode.j,currentNode.theta,action[0],action[1],red)

            for neighbourNode, newDistance in currentNode.neighbours.items():
                heapq.heappush(priorityQueue, (neighbourNode.cost, neighbourNode))

        return

    def isInTargetArea(self, i, j):
  
        if (i - self.endX) ** 2 + (j - self.endY) ** 2 - 0.01 <= 0:
            return True
        else:
            return False

    def backTrack(self, child):
        while child != None:
            path.append(child)
            print(child.i, child.j, "Path")
            child = child.parent
        return True

    
    def isAnObstacle(self, x, y):

        # Boundary condition
        if (x < 0) or (x > 10) or (y < 0) or (y > 10): 
            return True
        
        # Obstacle 1 (Circle Up)
        elif (x-2)**2 + (y-8)**2 - (1+self.cl)**2 <= 0:   
            return True
        
        # Obstacle 2 (Square) 
        elif x >= 0.25-self.cl and x <= 1.75+self.cl and y >= 4.25-self.cl and y <= 5.75+self.cl: 
            return True
        
        # Obstacle 3 (Rectangle Up)
        elif x >= 3.75-self.cl and x <= 6.25+self.cl and y >= 4.25-self.cl and y <= 5.75+self.cl:      
            return True
        
          # Obstacle 4 (Circle Down)
        elif (x-2)**2 + (y-2)**2 - (1+self.cl)**2 <= 0:                
            return True
        
        # Obstacle 3 (Rectangle Down)
        elif x >= 7.25-self.cl and x <= 8.75+self.cl and y >= 2-self.cl and y <= 4+self.cl:      
            return True
        
        # Node in Freespace
        else:
            return False 
        


    def isOutsideArena(self, x, y):

        return True if x < self.cl or y < self.cl or x > 10 - self.cl or y > 10 - self.cl else False


x1 = float(input("Enter the x coordinate of the starting point: "))
y1 = float(input("Enter the y coordinate of the starting point: "))
thetaStart = int(input("Enter the start theta: "))
print("#############################################")

x2 = float(input("Enter the x coordinate of the ending point: "))
y2 = float(input("Enter the y coordinate of the ending point: "))
print("#############################################")

RPM1 = float(input("Enter RPM1: "))
RPM2 = float(input("Enter RPM2 "))
radius = float(input("Enter the radius of the robot:  "))
cl = float(input("Enter the cl:  "))

#############################################
# Algorithm Driver
end = Node(x2, y2, x2, y2, 0)
start = Node(x1, y1, x2, y2, thetaStart)
start.costToCome = 0
robot = Graph(start, end, RPM1, RPM2, radius, cl)
path = []

# Check if path can be found
if robot.performAStar(start, end):
    pass
    pygame.init()  # Setup Pygame 
    gridDisplay = pygame.display.set_mode((w, h))
    pygame.display.set_caption("A* Algorithm")
    exiting = False
    clock = pygame.time.Clock()
    grid = [[0 for j in range(h)] for i in range(w)]
    canvas = Graph(start, end, RPM1, RPM2, radius, cl)
    canvas.generateGraph()
    robot.visualize(start, end)
    path.reverse()
else:
    # No Path Found
    exiting = True

while not exiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exiting = True

            # Visualizing the final path
    for index in range(len(path)-1):
        node = path[index]
        action = node.valid_actions[path[index+1]]
        robot.drawActionSet(node.i, node.j, node.theta, action[0], action[1], black)


    clock.tick(2000)
    pygame.display.flip()
    exiting = True
pygame.quit()
