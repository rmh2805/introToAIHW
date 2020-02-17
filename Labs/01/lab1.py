import heapq
import math
import sys

from PIL import Image

# ===================================================<Global State>=================================================== #
iceColor = (0x80, 0x80, 0xFF)
mudColor = (0x8E, 0x91, 0x0E)
leavesColor = (0xFE, 0xFE, 0xFE)

waterColor = (0x00, 0x00, 0xFF)
trailColor = (0x00, 0x00, 0x00)

pathColor = [(0x00, 0xFF, 0xFF), (0xFF, 0x00, 0xFF)]
waypointColor = (0xFF, 0xFF, 0x00)
startColor = (0xFF, 0x00, 0x00)

colorMap = {(0xF8, 0x94, 0x12): 'Open land',
            (0xFF, 0xC0, 0x00): 'Rough meadow',
            (0xFF, 0xFF, 0xFF): 'Easy movement forest',
            (0x02, 0xD0, 0x3C): 'Slow run forest',
            (0x02, 0x88, 0x28): 'Walk forest',
            (0x05, 0x49, 0x18): 'Impassible vegetation',
            (0x47, 0x33, 0x03): 'Paved road',
            (0xCD, 0x00, 0x65): 'Out of bounds',
            waterColor: 'Lake/Swamp/Marsh',
            trailColor: 'Footpath',
            leavesColor: 'Leaves',
            iceColor: 'Ice',
            mudColor: 'Mud'}

speedMap = {'Paved road': 1,
            'Footpath': 1,
            'Leaves': .85,
            'Open land': .8,
            'Easy movement forest': .7,
            'Slow run forest': .6,
            'Walk forest': .5,
            'Rough meadow': .4,
            'Mud': .3,
            'Ice': .2,
            'Impassible vegetation': 0,
            'Lake/Swamp/Marsh': 0,
            'Out of bounds': 0}


# ===============================================<Distance Calculation>=============================================== #
# Converts the horizontal distance from (x0, y0) to (xF, yF) in meters
def getHDist(x0, y0, xF, yF):
    return ((10.29 * (xF - x0)) ** 2 + (7.55 * (yF - y0)) ** 2) ** 0.5


# Calculates the vertical distance from (x0, y0) to (xF, yF)
def getVDist(x0, y0, xF, yF, heightArray):
    return heightArray[yF][xF] - heightArray[y0][x0]


# Calculates the straight line distance from (x0, y0) to (xF, yF)
def getDist(x0, y0, xF, yF, heightArray):
    return (getHDist(x0, y0, xF, yF) ** 2 + getVDist(x0, y0, xF, yF, heightArray) ** 2) ** .5


# ==================================================<Image Handling>================================================== #
def getTerrain(x, y, terrainData):
    global colorMap
    try:
        return colorMap[terrainData[y, x][0:3]]
    except KeyError:
        return 'Out of bounds'


# Sets the chosen pixel in pix to the chosen color
def drawPic(x, y, color, pix):
    pix[y, x] = color


# Redraws the map to represent the current season
def updateMap(season, terrainData):
    pass


# ==================================================<File Handling>=================================================== #
# noinspection PyTypeChecker
def parseElevation(elevationFile):
    eF = open(elevationFile, 'r')
    data = eF.readlines()
    eF.close()

    for i in range(0, len(data)):
        line = data[i].strip().split()
        for j in range(0, len(line)):
            line[j] = float(line[j])
        data[i] = line

    return data


# noinspection PyTypeChecker
def parsePath(pathFile):
    pF = open(pathFile, 'r')
    data = pF.readlines()
    pF.close()

    for i in range(0, len(data)):
        point = data[i].strip().split()
        temp = int(point[1])
        point[1] = int(point[0])
        point[0] = temp
        data[i] = point

    return data


# =================================================<Get Pacing Data>================================================== #
# An implementation of Tobler's hiking function for pace on a slope
def getVertPace(x0, y0, xF, yF, heightArray):
    hDist = getHDist(x0, y0, xF, yF)
    vDist = heightArray[yF][xF] - heightArray[y0][x0]
    return toblerPace(hDist, vDist)


def toblerPace(dX, dY):
    return math.e ** (3.5 * abs(dY / dX + 0.05))


def getTerrainSpeed(x, y, terrainData):
    return speedMap[getTerrain(x, y, terrainData)]


# ==================================================<Priority Queue>================================================== #
def enqueue(pQueue, node):
    pQueue.append(node)


def sortQueue(pQueue):
    pQueue.sort(key=lambda n: n.getF())


def dequeue(pQueue):
    return pQueue.pop(0)


# ===================================================<Image Search>=================================================== #
def findBorders(color, width, height, terrainData):
    visited = [[False for i in range(width)] for i in range(height)]

    queue = [(0, 0)]
    while len(queue) > 0:
        tup = queue.pop(0)
        getNeighbors(tup, terrainData, width, height)


# ===================================================<Path Search>==================================================== #


def moveWeight(parent, child, heightData, terrainData):
    x0 = parent.x
    y0 = parent.y
    xF = child.x
    yF = child.y

    terrainSpeed = (getTerrainSpeed(x0, y0, terrainData) + getTerrainSpeed(xF, yF, terrainData)) / 2
    if terrainSpeed == 0:
        return None

    dist = getHDist(x0, y0, xF, yF)
    vertPace = getVertPace(x0, y0, xF, yF, heightData)

    return dist * vertPace / terrainSpeed


class myNode:
    y = 0
    x = 0
    parent = None
    g = 0
    h = 0

    def __init__(self, x, y, tgtX, tgtY, parent, heightData, terrainData, hFunc):
        self.x = x
        self.y = y
        self.parent = parent
        if parent is not None:
            self.g = parent.g + moveWeight(parent, self, heightData, terrainData)
        else:
            self.g = 0
        self.h = hFunc(self, tgtX, tgtY)

    def __eq__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        elif isinstance(other, myNode):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def getF(self):
        return self.g + self.h


# Returns the time to reach destination with a straight line path of optimal slope and terrain (both values 1)
def straightLineH(node, tgtX, tgtY):
    return getHDist(node.x, node.y, tgtX, tgtY)


def visit(vMap, node):
    vMap[(node.x, node.y)] = node


def hasVisited(vMap, coords):
    if isinstance(coords, myNode):
        return (coords.x, coords.y) in vMap
    elif isinstance(coords, tuple) and len(coords) == 2:
        return coords in vMap
    else:
        return False


def getNeighbors(node, terrainData, width, height):
    if isinstance(node, myNode):
        nX = node.x
        nY = node.y
    elif isinstance(node, tuple):
        nX, nY = node
    else:
        return None

    neighbors = []
    for x in range(max(nX - 1, 0), min(nX + 2, width)):
        for y in range(max(nY - 1, 0), min(nY + 2, height)):
            if x == nX and y == nY:
                continue

            if getTerrainSpeed(x, y, terrainData) != 0:
                neighbors.append((x, y))

    return neighbors


def makePath(node):
    # todo: This
    path = []
    while node is not None:
        path.insert(0, node)
        node = node.parent

    return path


def aStar(startX, startY, tgtX, tgtY, heightData, terrainData, width, height, hFunc=straightLineH):
    startNode = myNode(startX, startY, tgtX, tgtY, None, heightData, terrainData, hFunc)

    visited = dict()
    visit(visited, startNode)

    pQueue = []
    enqueue(pQueue, startNode)

    while len(pQueue) > 0:
        node = dequeue(pQueue)

        if node == (tgtX, tgtY):
            return makePath(node), node.g

        neighbors = getNeighbors(node, terrainData, width, height)
        for neighbor in neighbors:
            if not hasVisited(visited, neighbor):
                nX, nY = neighbor
                neighbor = myNode(nX, nY, tgtX, tgtY, node, heightData, terrainData, hFunc)
                visit(visited, neighbor)
                enqueue(pQueue, neighbor)
            else:
                neighbor = visited[neighbor]
                adjWeight = moveWeight(node, neighbor, heightData, terrainData) + node.g
                if neighbor.g > adjWeight:
                    neighbor.g = adjWeight
                    neighbor.parent = node
                    enqueue(pQueue, neighbor)

        sortQueue(pQueue)


# ==================================================<Main Execution>================================================== #
def main(terrainFile, elevationFile, pathFile, season, outputFile):
    # Parse files into useful forms
    im = Image.open(terrainFile)
    pix = im.load()  # Used to scan the final image, column-major
    elevationData = parseElevation(elevationFile)  # The elevation of all pixels, row-major
    waypoints = parsePath(pathFile)  # The coordinates of all points to reach

    # Assuming equal [0, 0] (top left), grab max col and row (width and height) with data for both terrain and elevation
    width = min(im.width, len(elevationData[0]))
    height = min(im.height, len(elevationData))

    findBorders(waterColor, width, height, pix)

    # path = []
    # totalTime = 0
    # for i in range(1, len(waypoints)):
    #     segment, time = aStar(waypoints[i - 1][0], waypoints[i - 1][1], waypoints[i][0], waypoints[i][1],
    #                           elevationData, pix,
    #                           width, height)
    #     path.append(segment)
    #     totalTime += time
    #
    # for i in range(0, len(path)):
    #     color = pathColor[i % len(pathColor)]
    #     for pixel in path[i]:
    #         drawPic(pixel.x, pixel.y, color, pix)
    #
    # for waypoint in waypoints:
    #     drawPic(waypoint[0], waypoint[1], waypointColor, pix)
    #
    # drawPic(waypoints[0][0], waypoints[0][1], startColor, pix)
    #
    # im.save(outputFile)


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if argc != 6:
        print('Usage: python3 ' + argv[0] + ' <Terrain File> <Elevation File> <Path File> <Season> <Output File>')
        exit(1)

    main(argv[1], argv[2], argv[3], argv[4], argv[5])
