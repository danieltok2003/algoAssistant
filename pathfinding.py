from tkinter import *
import threading
import time


gridHeight = 30
gridWidth = 30

cellHeight = 15
cellWidth = 15

VISITED = 'red'
MARK = 'orange'
PATH = 'purple'
START = 'green'
TARGET = 'blue'
EMPTY = 'white'
BLOCK = 'black'
grid = {}  # grid = { [xCoord, yCoord]: [dimensions] }
wallsFile = 'walls'
timing = 0

file = 'studentSession'


def createGrid():
    global grid
    rootX = 0
    rootY = 0
    for y in range(gridHeight):
        for x in range(gridWidth):
            window.create_rectangle(rootX, rootY, rootX + cellWidth, rootY + cellHeight, fill=EMPTY, outline='black')  # draw square on screen
            window.pack()
            grid[x, y] = [rootX, rootY, rootX + cellWidth, rootY + cellHeight]  # add square to grid edges
            rootX += cellWidth  # offset for next horizontal cell
        rootY += cellHeight  # offset for next row
        rootX = 0  # return x offset to 0 for new row


def paintCoords(x, y, coordType):  # handles painting of start, target, mark, path, visited, and obstacle cells
    color = ''
    if coordType == 'startCoords':
        color = START
        setStartButton["state"] = "disabled"
    elif coordType == 'targetCoords':
        color = TARGET
        setTargetButton["state"] = "disabled"


    elif coordType == 'markCoords':
        color = MARK
    elif coordType == 'pathCoords':
        color = PATH
    elif coordType == 'visitedCoords':
        color = VISITED
    elif coordType == 'blockCoords':
        color = BLOCK
    try:
        window.create_rectangle(grid[(x, y)][0], grid[(x, y)][1], grid[(x, y)][2],
                            grid[(x, y)][3], fill=color, outline='black')
    except KeyError:
        print('Out of range coordinates entered')

    window.pack()


def getStartCoords():
    try:
        paintCoords(int(startXcoord.get()), int(startYcoord.get()), 'startCoords')
    except ValueError:
        print('Invalid coordinates entered')


def getTargetCoords():
    try:
        paintCoords(int(targetXcoord.get()), int(targetYcoord.get()), 'targetCoords')
    except ValueError:
        print('Invalid coordinates entered')


def backTrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])  # backtracking through parents from goal node until start node found
    path.reverse()  # reversing path to get start --> end
    return path


def calculateEdges():
    nodes = list(grid.keys())
    edges = {}  # dictionary where {node : [neighbour1, neighbour2, neighbour3, neighbour 4] }
    for node in nodes:
        try:
            for neighbour in nodes:
                if (abs(neighbour[0] - node[0]) == 1 and abs(neighbour[1] - node[1]) == 0) or (abs(neighbour[0] - node[0]) == 0 and abs(neighbour[1] - node[1]) == 1):  # "look" around all 4 neighbouring nodes
                    if node not in edges.keys():  # add unvisited node to marked nodes
                        edges[node] = [neighbour]
                    else:
                        edges[node].append(neighbour)  # add marked node to visited nodes
        except IndexError:
            continue
    return edges


def drawObstacles(edges):
    with open(wallsFile, 'r') as walls:
        coords = walls.readline().split(" ")
    for coord in coords:
        x = int(coord[: coord.index(',')])
        y = int(coord[coord.index(',') + 1:])
        paintCoords(x, y, 'blockCoords')
        if (x, y) in edges:
            del edges[(x, y)]  # delete nodes where obstacles have been drawn
            for neighbours in edges.values():
                if (x, y) in neighbours:
                    neighbours.remove((x, y))


def background_bfs():
    threading.Thread(target=bfs).start()


def background_dfs():  # multithreading to allow window to keep updating with each iteration
    threading.Thread(target=dfs).start()


def bfs():
    try:
        start = (int(startXcoord.get()), int(startYcoord.get()))  # extracting input from entry boxes
        target = (int(targetXcoord.get()), int(targetYcoord.get()))
    except ValueError:
        print('Input cannot be blank or string')
        return 0

    if testInputRange(start, target) is True:
        print('Out of range input coordinates')
        return 0

    explored = []
    queue = [start]
    parent = {}
    edges = calculateEdges()  # gathering all valid edges
    print('To draw obstacles, write coords to the walls.txt file')

    drawObstacles(edges)  # painting and removing obstacle edges

    found = False
    while found is False:
        for _ in queue:
            presentNode = queue[0]

            if presentNode not in explored:
                if presentNode != start and presentNode != target:
                    paintCoords(presentNode[0], presentNode[1], 'visitedCoords')  # mark current node as visited
                neighbours = edges[presentNode]  # get all nodes of current visited node
                if presentNode == target:  # if found, begin backtracking
                    found = True
                    for node in backTrace(parent, start, target):
                        if node != start and node != target:
                            paintCoords(node[0], node[1], 'pathCoords')  # draw path from start to end
                            time.sleep(0.01)  # slow down for path reveal
                    break
                for neighbour in neighbours:
                    if neighbour not in explored:
                        parent[neighbour] = presentNode
                        queue.append(neighbour)  # add neighbour of current node to queue
                        if neighbour != target:
                            paintCoords(neighbour[0], neighbour[1], 'markCoords')  # paint it as marked as haven't yet visited marked node

                    else:
                        if neighbour != start:
                            paintCoords(neighbour[0], neighbour[1], 'visitedCoords')  # as has been explored, mark as visited
                explored.append(presentNode)  # add marked node to nodes that have been explored to be converted to visited on next iteration

            queue.pop(0)  # remove front node from queue
            time.sleep(timing)

    bfsButton["state"] = "disabled"

def testInputRange(start, target):
    return start not in grid.keys() or target not in grid.keys()



def dfs():
    try:
        start = (int(startXcoord.get()), int(startYcoord.get()))  # extracting input from entry boxes
        target = (int(targetXcoord.get()), int(targetYcoord.get()))
    except ValueError:
        print('Input cannot be blank or string')
        return 0

    if testInputRange(start, target) is True:
        print('Out of range input coordinates')
        return 0

    explored = []
    queue = [start]
    parent = {}
    edges = calculateEdges()
    print(edges)

    drawObstacles(edges)  # painting and removing obstacle edges

    found = False
    while found is False:
        for _ in queue:
            presentNode = queue[0]
            if presentNode not in explored:
                neighbours = edges[presentNode]
                if presentNode != start and presentNode != target:
                    paintCoords(presentNode[0], presentNode[1], 'visitedCoords')

                if presentNode == target:
                    found = True
                    for node in backTrace(parent, start, target):
                        if node != start and node != target:
                            paintCoords(node[0], node[1], 'pathCoords')
                            time.sleep(0.01)  # slow down for path reveal
                    break
                for neighbour in neighbours:
                    if neighbour not in explored:
                        parent[neighbour] = presentNode
                        queue.insert(0, neighbour)
                        if neighbour != target and neighbour != start:
                            paintCoords(neighbour[0], neighbour[1], 'markCoords')
                    else:
                        if neighbour != start:
                            paintCoords(neighbour[0], neighbour[1], 'visitedCoords')
                explored.append(presentNode)
            queue.pop()  # popping node from top of stack
            time.sleep(timing)

    dfsButton["state"] = "disabled"


def timeControl(timeInterval):
    global timing
    timing = timeInterval


def refresh():
    master.destroy()
    main()


def uploadTime():
    with open(file, 'w') as studentSession:  # opening as 'w' clears file for new session
        studentSession.write('0' + '\n')
        studentSession.write('0' + '\n')
        studentSession.write(str(round(time.time() - start_time, 0)) + '\n')
        studentSession.close()
    master.destroy()


def main():
    global master
    global window
    global startXcoord
    global startYcoord
    global targetXcoord
    global targetYcoord
    global setTargetButton
    global setStartButton
    global bfsButton
    global dfsButton
    global start_time
    start_time = time.time()
    master = Tk()
    master.resizable(False, False)
    window = Canvas(master, width=800, height=600)

    startXcoord = Entry(master)
    startYcoord = Entry(master)

    setStartButton = Button(master, height=1, width=15, text='Set start coords', command=getStartCoords)
    targetXcoord = Entry(master)
    targetYcoord = Entry(master)
    setTargetButton = Button(master, height=1, width=15, text='Set target coords', command=getTargetCoords)
    bfsButton = Button(master, height=1, width=15, text='BFS', command=background_bfs)
    dfsButton = Button(master, height=1, width=15, text='DFS', command=background_dfs)

    slow = Button(master, height=1, width=15, text='Slow', command=lambda: timeControl(0.5), bg='green')
    medium = Button(master, height=1, width=15, text='Medium', command=lambda: timeControl(0.1), bg='green')
    fast = Button(master, height=1, width=15, text='Fast', command=lambda: timeControl(0), bg='green')

    reset = Button(master, height=1, width=15, text='Reset', command=refresh)
    exitButton = Button(master, text="Save work", command=uploadTime)

    master.title(f'{gridWidth} x {gridHeight} grid')
    master.after(0, createGrid)

    startXcoord.pack()

    startYcoord.pack()

    setStartButton.pack()

    targetXcoord.pack()

    targetYcoord.pack()

    setTargetButton.pack()

    bfsButton.pack()

    dfsButton.pack()

    slow.pack()
    medium.pack()
    fast.pack()

    reset.pack()

    exitButton.pack()

    master.mainloop()


if __name__ == "__main__":

    main()
