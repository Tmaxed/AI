import heapq
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Process

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        if(self.f == other.f):
            return self.g > other.g
        else:
            return self.f < other.f

    def __gt__(self, other):
        if(self.f == other.f):
            return self.g > other.g
        else:
            return self.f > other.f

    def __eq__(self, other):
        return self.f == other.f

def checkClose(node, list):
    for item in list:
        if node.position == item.position:
            return 1

    return 0

def checkOpen(node, list):
    for item in list:
        if node.position == item.position:
            return 1

    return 0

def checkImp(node, list):
    for item in list:
        if node.position == item:
            return 1

    return 0

def AForward(maze, start, goal, impass):

    #setup base nodes
    search_time = time.time_ns() // 1000000
    startN = Node(None, start)
    startN.g = startN.h = startN.f = 0
    endN = Node(None, goal)
    endN.g = endN.h = endN.f = 0

    #setup lists
    open = [] #This will be a min heap
    closed = []
    path = []

    #push start node onto heap
    heapq.heappush(open, startN)

    #enter execution loop
    iter = 0
    while(1):

        #This is to detect an unsolvable maze, returns empty list
        if(len(open) == 0):
            return path

        #Grab the current node, or rather 'pop' the heap. Add node to closed list
        currentN = heapq.heappop(open)
        closed.append(currentN)

        #checks if we just expanded the goal node,
        #if yes it follows the tree nodes from goal node to the beginning node which serves as our path
        if(currentN.position == endN.position):
            current = currentN
            while current is not None:
                path.append(current.position)
                current = current.parent

            print("\nPath search took %s milli seconds ---" % (time.time_ns() // 1000000  - search_time))
            return path[::-1] #Return reversed path

        #generate successors, check adjacent nodes
        success = []
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent square offsets
            #calc node coords
            nodePos = (currentN.position[0] + new_pos[0], currentN.position[1] + new_pos[1])

            #checking X and Y values against maze bounds to make sure its actually in the maze
            if nodePos[0] > (len(Z) - 1) or nodePos[0] < 0 or nodePos[1] > (len(Z[len(Z)-1]) -1) or nodePos[1] < 0:
                continue #move onto next successor

            #if it passes, create new node so it can be checked against other Node based structures
            newSucc = Node(currentN, nodePos)

            #check if it is marked as impassable
            if(checkImp(newSucc, impass)):
                continue

            #check if present in closed list
            if(checkClose(newSucc, closed)):
                continue

            #assign the nodes attribute values
            newSucc.g = currentN.g + 1
            newSucc.h = abs(newSucc.position[0] - endN.position[0]) + abs(newSucc.position[1] - endN.position[1])
            newSucc.f = newSucc.g + newSucc.h

            #checks if already within the open list
            if(checkOpen(newSucc, open)):
                continue

            #push it onto the heap and move on to next adjacent cell
            heapq.heappush(open, newSucc)

def isPres(pos):
    for mem in impass:
        if(mem == pos):
            return 1

    return 0

def wallFind(pos, maze):
    #wall_time = time.time_ns() // 1000000
    wallList = []
    for posOffset in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        currPos = (pos[0] + posOffset[0], pos[1] + posOffset[1])

        #check if we arleady know about it
        if(isPres(currPos) == 1):
            continue


        #check if node is out of bounds
        if currPos[0] > (len(Z) - 1) or currPos[0] < 0 or currPos[1] > (len(Z[len(Z)-1]) -1) or currPos[1] < 0:
            continue

        #next just check if its a wall
        if(int(maze[currPos[0]][currPos[1]]) == 1):
            impass.append(currPos)
            X[currPos[0]][currPos[1]] = 1
            #plt.pcolormesh(X)
            #plt.pause(.001)

    #print("\nsurrounding wall search took %s milli seconds ---" % (time.time_ns() // 1000000  - wall_time))
    return

if __name__ == "__main__":
    randOrBt = (sys.argv[1])
    gry = int(sys.argv[2])
    plt.axes().invert_yaxis()
    plt.ion()

    number = 0
    interv = 0
    if(randOrBt == "random"):
        number = 0
        interv = 5
    elif(randOrBt == "backtrack"):
        number = 50
        interv = 25
    else:
        print("invalid input\n")
        sys.exit()


    totalTime = 0
    #This loop moves through different mazes to test
    while(number < (number + 50)):

        #sets start time
        start_time = time.time()

        #generates second matrix used to display agent progression visually for debug purposes
        X = np.random.choice([0, 1, 2], size=[101, 101], p=[1, 0, 0])

        #generates the actual matrix we will be moving the agent through
        Z = np.random.choice([0, 1, 2], size=[101, 101], p=[1, 0, 0])

        if(randOrBt == "random"):
            fp = open("arrs/randGrid/{0:0=2d}.txt".format(number), 'r') #open file containing maze matrix
        elif(randOrBt == "backtrack"):
            fp = open("arrs/backTrackerMazes/{0:0=2d}.txt".format(number), 'r') #open file containing maze matrix
        else:
            print("invalid input\n")

        count = 0
        #this loop loads the maze data from file into Z line by line
        while True:
            # Get next line from file
            line = fp.readline()

            # if line is empty, EOF
            if not line:
                break

            Z[count] = line.strip().split(' ')
            count += 1

        #set the start and goal points
        start = (0,0)
        goal = (100,100)

        found = 0
        count = 0

        impass = [] #list that stores discovered impassable terrain
        #This loop is the heart of the agent behavior
        #it requests a path, walks the path until it finds a wall, then it requests a new path
        #repeat until agent makes it to goal
        while(found == 0):
            count+=1
            if(gry and count % interv == 0):
                plt.pcolormesh(X)
                plt.pause(.001)


            #first checks the agents surrounding for walls before doing anything
            wallFind((start[0], start[1]), Z) #checks surrounding nodes, adds any walls found to impass list

            #request an initial path from current position(start) to goal(100,100)
            path = AForward(Z, start, goal, impass)

            #checks if path is empty, ie there is no possible path to goal
            if(len(path) == 0):
                print("No path available!\n", len(path))
                X[goal[0]][goal[1]] = 5
                X[0][0] = 5
                plt.pcolormesh(X)
                timet = time.time() - start_time
                print("\nMaze#", number, " Took this many seconds: ", timet)
                totalTime = totalTime + timet
                start_time = 0
                plt.savefig("pics/solutions/maze{0:0=2d}s.png".format(number))
                found = 1
                number+=1

            val = 0
            #Received a valid path, so the agent starts walking it
            while(val < len(path)):

                currentPos = path[val]
                check = int((Z[currentPos[0]][currentPos[1]])) #stores 0 or 1, depending on if currentPos is a wall or not
                if(check == 1):
                    #Hit a wall, so we add it to impass, then request a new path a step backwards from here
                    X[currentPos[0]][currentPos[1]] = 1
                    impass.append(currentPos)
                    start = path[val - 1]
                    check = 0
                    break #once a wall is found, the current path is no good. Break loop and get a new path
                elif(currentPos == goal):
                    #Made it to the goal, so calculate runtime and save figure and setup variables for the next maze
                    X[goal[0]][goal[1]] = 5
                    X[0][0] = 5
                    plt.pcolormesh(X)
                    plt.pause(.001)
                    #print("\n\nMade it!")
                    timet = time.time() - start_time
                    print("\nTook this many seconds: ", timet)
                    totalTime = totalTime + timet
                    start_time = 0
                    plt.savefig("pics/solutions/maze{0:0=2d}s.png".format(number))
                    found = 1
                    check = 0
                    number+=1
                    break
                else:
                    #took a clean step, can keep going on current route(loop will loop)
                    X[currentPos[0]][currentPos[1]] = 2
                    check = 0
                    val += 1

                    #check for walls in current agent visiblility range
                    wallFind((currentPos[0], currentPos[1]), Z)


    print("Average time: ", totalTime/50)
    plt.ioff()
