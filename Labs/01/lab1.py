import math
import sys

from PIL import Image

# ===================================================<Global State>=================================================== #
# ============================================<Files>============================================= #
terrainImage = None  # Kind of, anyway

# ===========================================<Map Data>=========================================== #
elevationData = None
terrainData = None
mapWidth = -1
mapHeight = -1

# =========================================<Color Data>========================================== #
# Used for seasonal changes
iceColor = (0x80, 0x80, 0xFF)
mudColor = (0x8E, 0x91, 0x0E)
leavesColor = (0xFE, 0xFE, 0xFE)

# Referenced but present by default
waterColor = (0x00, 0x00, 0xFF)
trailColor = (0x00, 0x00, 0x00)

# Used to draw final path
pathColor = [(0x00, 0xFF, 0xFF), (0xFF, 0x00, 0xFF)]
waypointColor = (0xC0, 0xC0, 0x00)
startColor = (0xFF, 0x00, 0x00)

# Map color codes onto terrain types
colorTerrainMap = {(0xF8, 0x94, 0x12): 'Open land',
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

# =============================================<Misc>============================================= #
# Map terrain types to effective speed over them
terrainSpeedMap = {'Paved road': 1,
                   'Footpath': 1,
                   'Leaves': .75,
                   'Open land': .75,
                   'Easy movement forest': .75,
                   'Slow run forest': .6,
                   'Walk forest': .4,
                   'Rough meadow': .4,
                   'Mud': .3,
                   'Ice': .2,
                   'Impassible vegetation': 0,
                   'Lake/Swamp/Marsh': 0,
                   'Out of bounds': 0}


def h(start, tgt):
    return getHDist(start[0], start[1], tgt[0], tgt[1])


# ==================================================<File Handlers>=================================================== #
def writeImage(outputFile):
    global terrainImage
    terrainImage.save(outputFile)


def initializeTerrain(terrainFile):
    global terrainImage, terrainData, mapWidth, mapHeight
    terrainImage = Image.open(terrainFile)
    terrainData = terrainImage.load()

    if mapWidth == -1:
        mapWidth, mapHeight = terrainImage.size
    else:
        mapWidth = min(mapWidth, terrainImage.width)
        mapHeight = min(mapHeight, terrainImage.height)


# noinspection PyTypeChecker
def parseElevation(elevationFile):
    global elevationData, mapWidth, mapHeight
    eF = open(elevationFile)
    elevationData = eF.readlines()
    eF.close()

    for rowI in range(0, len(elevationData)):
        row = elevationData[rowI].strip().split()
        for colI in range(0, len(row)):
            row[colI] = float(row[colI])
        elevationData[rowI] = row

    if mapWidth == -1:
        mapWidth = len(elevationData[0])
        mapHeight = len(elevationData)
    else:
        mapWidth = min(mapWidth, len(elevationData[0]))
        mapHeight = min(mapHeight, len(elevationData))


# noinspection PyTypeChecker
def parsePath(pathFile):
    pF = open(pathFile)
    data = pF.readlines()
    pF.close()

    for i in range(0, len(data)):
        waypoint = data[i].strip().split()
        data[i] = (int(waypoint[1]), int(waypoint[0]))

    return data


def getHeight(row, col):
    global elevationData
    return elevationData[row][col]


# ==================================================<Global Access>=================================================== #
def putColor(row, col, color):
    terrainData[col, row] = color


def getColor(row, col):
    return terrainData[col, row][0:3]


def getTerrain(row, col):
    try:
        return colorTerrainMap[getColor(row, col)]
    except KeyError:
        return 'Out of bounds'


# ====================================================<Math Utils>==================================================== #
def getAdj(row, col):
    global mapWidth, mapHeight
    adj = []
    for aRow in range(max(row - 1, 0), min(row + 2, mapHeight)):
        for aCol in range(max(col - 1, 0), min(col + 2, mapWidth)):
            adj.append((aRow, aCol))
    adj.remove((row, col))
    return adj


# Converts the horizontal distance from (x0, y0) to (xF, yF) in meters
def getHDist(row0, col0, rowF, colF):
    return ((10.29 * (colF - col0)) ** 2 + (7.55 * (rowF - row0)) ** 2) ** 0.5


# Calculates the vertical distance from (x0, y0) to (xF, yF)
def getVDist(row0, col0, rowF, colF):
    return getHeight(rowF, colF) - getHeight(row0, col0)


# Calculates the straight line distance from (x0, y0) to (xF, yF)
def getDist(row0, col0, rowF, colF):
    return (getHDist(row0, col0, rowF, colF) ** 2 + getVDist(row0, col0, rowF, colF) ** 2) ** .5


# ==================================================<Cost Functions>================================================== #
def toblerPace(dX, dY):
    if dX == 0:
        return 0
    return math.e ** (3.5 * abs(dY / dX + 0.05))


def getTerrainSpeed(coords):
    try:
        return terrainSpeedMap[getTerrain(coords[0], coords[1])]
    except KeyError:
        return 0


def costMultiplier(start, tgt):
    hDist = getHDist(start[0], tgt[0], start[1], tgt[1])
    vDist = getVDist(start[0], tgt[0], start[1], tgt[1])

    terrainSpeed = (getTerrainSpeed(start) + getTerrainSpeed(tgt)) / 2
    return toblerPace(hDist, vDist) / terrainSpeed


def moveCost(start, tgt):
    return getHDist(start[0], start[1], tgt[0], tgt[1]) * costMultiplier(start, tgt)


# =================================================<Search Functions>================================================= #
class myNode:
    coords = None
    row = 0
    col = 0
    parent = None
    g = 0
    h = 0

    def __init__(self, coords, tgt, parent=None):
        self.coords = coords
        self.row, self.col = coords

        self.parent = parent
        if parent is not None:
            self.g = parent.g + moveCost(parent.coords, coords)
        else:
            self.g = 0

        self.h = h(coords, tgt)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.coords == other
        elif isinstance(other, myNode):
            return self.coords == other.coords
        else:
            return False

    def getF(self):
        return self.g + self.h


def getNeighbors(node):
    result = []
    for adj in getAdj(node.row, node.col):
        if getTerrainSpeed(adj) != 0:
            result.append(adj)

    return result


def aStar(startPoint, endPoint):
    startNode = myNode(startPoint, endPoint)

    visited = {startNode.coords: startNode}
    pQueue = [startNode]

    while len(pQueue) > 0:
        node = pQueue.pop(0)

        if node == endPoint:
            return makePath(node)

        for neighbor in getNeighbors(node):
            if neighbor not in visited:
                neighborNode = myNode(neighbor, endPoint, node)
                visited[neighbor] = neighborNode
                pQueue.append(neighborNode)
            else:
                neighborNode = visited[neighbor]
                altG = moveCost(node.coords, neighbor) + node.g
                if altG < neighborNode.g:
                    neighborNode.g = altG
                    neighborNode.parent = node
                    pQueue.append(neighborNode)

        pQueue.sort(key=lambda n: n.getF())

    return None


def makePath(node):
    path = []
    while node is not None:
        path.insert(0, node.coords)
        node = node.parent
    return path


# ==================================================<Main Execution>================================================== #
def main(terrainFile, elevationFile, pathFile, season, outputFile):
    parseElevation(elevationFile)
    initializeTerrain(terrainFile)
    waypoints = parsePath(pathFile)

    path = []
    for i in range(1, len(waypoints)):
        path.append(aStar(waypoints[i - 1], waypoints[i]))

    for i in range(0, len(path)):
        for step in path[i]:
            putColor(step[0], step[1], pathColor[i % len(pathColor)])

    for waypoint in waypoints:
        putColor(waypoint[0], waypoint[1], waypointColor)
    putColor(waypoints[0][0], waypoints[0][1], startColor)
    writeImage(outputFile)


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if argc != 6:
        print('Usage: python3 ' + argv[0] + ' <Terrain File> <Elevation File> <Path File> <Season> <Output File>')
        exit(1)

    main(argv[1], argv[2], argv[3], argv[4], argv[5])
