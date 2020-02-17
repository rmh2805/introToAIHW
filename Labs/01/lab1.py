import math
import sys

from PIL import Image

iceColor = (0x80, 0x80, 0xFF)
mudColor = (0x8E, 0x91, 0x0E)

pathColor = (0xFF, 0x00, 0x00)

colorMap = {(0xF8, 0x94, 0x12): 'Open land',
            (0xFF, 0xC0, 0x00): 'Rough meadow',
            (0xFF, 0xFF, 0xFF): 'Easy movement forest',
            (0x02, 0xD0, 0x3C): 'Slow run forest',
            (0x02, 0x88, 0x28): 'Walk forest',
            (0x05, 0x49, 0x18): 'Impassible vegetation',
            (0x00, 0x00, 0xFF): 'Lake/Swamp/Marsh',
            (0x47, 0x33, 0x03): 'Paved road',
            (0x00, 0x00, 0x00): 'Footpath',
            (0xCD, 0x00, 0x65): 'Out of bounds',
            iceColor: 'Ice',
            mudColor: 'Mud'}

speedMap = {'Open land': .8,
            'Rough meadow': .5,
            'Easy movement forest': .75,
            'Slow run forest': .6,
            'Walk forest': .4,
            'Impassible vegetation': 0,
            'Lake/Swamp/Marsh': 0,
            'Paved road': 1,
            'Footpath': .9,
            'Out of bounds': 0,
            'Ice': .5,
            'Mud': .5}


# Converts a horizontal distance from pixels to meters
def getDist(deltaX, deltaY):
    return 10.29 * abs(deltaX) + 7.55 * abs(deltaY)


def getTerrain(x, y, terrainData):
    global colorMap
    try:
        return colorMap[terrainData[y, x][0, 3]]
    except KeyError:
        return None


# An implementation of Tobler's hiking function for pace
def getVertPace(x0, y0, xF, yF, heightArray):
    hDist = getDist(xF - x0, yF - y0)
    vDist = heightArray[xF][yF] - heightArray[x0][y0]
    return math.e ** (3.5 * abs(vDist / hDist + 0.05))


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


def main(terrainFile, elevationFile, pathFile, season, outputFile):
    im = Image.open(terrainFile)
    pix = im.load()
    elevationData = parseElevation(elevationFile)
    waypoints = parsePath(pathFile)

    # Assuming equal [0, 0] (top left), grab max col and row (width and height) with data for both terrain and elevation
    width = min(im.width, len(elevationData[0]))
    height = min(im.height, len(elevationData))

    # Mark the waypoints on the map
    for point in waypoints:
        print(point)
        pix[point[1], point[0]] = pathColor

    im.save(outputFile)


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if argc != 6:
        print('Usage: python3 ' + argv[0] + ' <Terrain File> <Elevation File> <Path File> <Season> <Output File>')
        exit(1)

    main(argv[1], argv[2], argv[3], argv[4], argv[5])
