import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import random
import math
import copy


pygame.init()

screenWidth = 800 
screenHeight = 800
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Cave Generator")

dirt = pygame.image.load("dirt.png")


'''

    EXPLANATION

    Splits the board (200 by 200 tiles) into 16 different regions; 4 down 4 across

    Each region has a 2/3 chance of having a large node.

    After all Large nodes are populated they have a 100% chance of connecting to their closest
    neighbour and a 66% chance of connecting to their second closest neighbour.

    Math is done to draw a 1 thick line to represent these connections.

    Program then thickens the caves by iterating 3 times. Each iteration there is a 50% chance a block is
    added west of an already existing block, 50% chance for east and same chance for north and south.

    Then do small nodes. Board is split into 64 regions with each region having a 50% chance for small node.

    Small nodes have 100% chance of connecting to closest neighbour and 50% chance of connecting to second
    closest neighbour.

    Then thicken by iterating 2 more times. This means large caves are 5 thick while small caves are 2 thick.


'''

def show_progress_bar(gameBoard):
    #for i in range(200):
    #    for j in range(200):
    #        if gameBoard[i][j]:
    #            win.blit(dirt,(i*4,j*4))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    
def custom_div(x,y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0

def gameBoardGen(gameBoard):
    for i in range(200):
        gameBoard.append(list())
        for j in range(200):
            gameBoard[i].append(0)
            # 1 is dirt, 0 is nothing

def getLargeNodes(largeNodes):
    for i in range(4): 
        for j in range(4): # so 16 total nodes
            if random.randint(0,3) != 0:
                ranNumH = random.randint(0,screenHeight/16)
                ranNumW = random.randint(0,screenWidth/16)
                nodeWidth = ((screenWidth/16)*i + ranNumW)*4
                nodeHeight = ((screenHeight/16)*j + ranNumH)*4
                node = (nodeWidth, nodeHeight)
                largeNodes.append(node)

def getSmallNodes(smallNodes):
    for i in range(8): 
        for j in range(8): # so 64 total nodes
            if random.randint(0,2) != 0:
                ranNumH = random.randint(0,int(200/64))
                ranNumW = random.randint(0,int(200/64))
                nodeWidth = ((200/64)*i + ranNumW)*32
                nodeHeight = ((200/64)*j + ranNumH)*32
                node = (nodeWidth, nodeHeight)
                smallNodes.append(node)
                
def getClosestTwoNodes(node, nodeList):
    # distance = sqrt((x2-x1)^2 + (y2-y1)^2)

    firstClosest = [(0,0), 999]
    secondClosest = [(0,0), 999]

    for nodeIter in nodeList:
        if nodeIter != node:
            distance = math.sqrt(math.pow(node[0]-nodeIter[0],2) + math.pow(node[1]-nodeIter[1],2))
            if distance < firstClosest[1]:
                firstClosest[0] = nodeIter
                firstClosest[1] = distance
            elif distance < secondClosest[1]:
                secondClosest[0] = nodeIter
                secondClosest[1] = distance
    
    return firstClosest[0],secondClosest[0]
    
def connectNodes(nodeList, gameBoard, connectChance):

    connections = set()

    for node in nodeList:
        firstClosest, secondClosest = getClosestTwoNodes(node, nodeList)
        connections.add((node, firstClosest))
        if random.randint(0,connectChance) != 0:
            connections.add((node, secondClosest))

    #print(connections)
    
    for connection in connections:
        
        # m = (y2-y1)/(x2-x1) is gradient equation
        gradient = custom_div((connection[1][1]-connection[0][1]),(connection[1][0]-connection[0][0]))
        
        # b = y-(m*x) is y intercept equation
        yinter = connection[1][1]-(gradient*connection[1][0])
        show_progress_bar(gameBoard)
        for i in range(800):
                
            for j in range(800):
                # check both if y = mx+b is true AND x = (y-b)/m because of float -> int accuracy
                if j == int(gradient*i + yinter) or i == int(custom_div((j-yinter),gradient)):
                    if ( i > connection[1][0] and connection[0][0] > i) or ( i < connection[1][0] and connection[0][0] < i):
                        if ( j > connection[1][1] and connection[0][1] > j) or ( j < connection[1][1] and connection[0][1] < j):
                            gameBoard[int(i/4)][int(j/4)] = 1

def thickenCaves(gameBoard, thickenAmount):

    n = thickenAmount #thicken n times
    
    for k in range(n):
        tempGameBoard = copy.deepcopy(gameBoard)
        show_progress_bar(gameBoard)
        for i in range(200):
            
            for j in range(200):
                
                if tempGameBoard[i][j] == 1:
                    for direction in range(4):
                        if random.randint(0,1) != 0:
                            # try loop is used to catch out of bounds array accessing
                                if direction == 0 and j-1 >= 0:
                                    gameBoard[i][j-1] = 1
                                elif direction == 1 and j+1 < 200:
                                    gameBoard[i][j+1] = 1
                                elif direction == 2 and i+1 < 200:
                                    gameBoard[i+1][j] = 1
                                elif direction == 3 and i-1 >= 0:
                                    gameBoard[i-1][j] = 1

def prettifyGameBoard(gameBoard):

    # removes all blocks that are surrounded by air or air surrounded by dirt
    # and 50% of blocks that have 3 sides of air and vice versa
    show_progress_bar(gameBoard)
    for i in range(200):
        for j in range(200):
            try: # try loop just catches accessing an array out of bounds
                if gameBoard[i][j]:
                    if not gameBoard[i-1][j] and not gameBoard[i+1][j] and not gameBoard[i][j-1] and not gameBoard[i][j+1]:
                        gameBoard[i][j] = 0

                    elif gameBoard[i-1][j] + gameBoard[i+1][j] + gameBoard[i][j-1] + gameBoard[i][j+1] == 1:
                        if random.randint(0,1) != 0:
                            gameBoard[i][j] = 0
                elif not gameBoard[i][j]:
                    if gameBoard[i-1][j] and gameBoard[i+1][j] and gameBoard[i][j-1] and gameBoard[i][j+1]:
                        gameBoard[i][j] = 1
                        
                    elif gameBoard[i-1][j] + gameBoard[i+1][j] + gameBoard[i][j-1] + gameBoard[i][j+1] == 3:
                        if random.randint(0,1) != 0:
                            gameBoard[i][j] = 1
            except:
                pass
    
# 200 by 200 array
gameBoard = list()
gameBoardGen(gameBoard)

largeNodes = list()
getLargeNodes(largeNodes)

smallNodes = list()
getSmallNodes(smallNodes)

largeChanceToConnect = 3# num is 1 - 1/x. for example if 3 then chance is 2/3
connectNodes(largeNodes, gameBoard, largeChanceToConnect)
thickenCaves(gameBoard, 2)

smallChanceToConnect = 2
connectNodes(smallNodes, gameBoard, smallChanceToConnect)

thickenCaves(gameBoard, 3)

prettifyGameBoard(gameBoard)

running = True
while running:


    
    for node in smallNodes:
        #print((node[0]*4,node[1]*4))
        pass#win.blit(dirt,(node[0]*32,node[1]*32))

    for i in range(200):
        for j in range(200):
            if gameBoard[i][j]:
                win.blit(dirt,(i*4,j*4))



    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
