import math

from PIL import Image

iceColor = (0x80, 0x80, 0xFF)
mudColor = (0x8E, 0x91, 0x0E)

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


def getTerrain(colorTuple):
    global colorMap
    return colorMap[colorTuple[0, 3]]


# An implementation of Tobler's hiking function for pace
def getRawPace(x0, y0, xF, yF, heightArray):
    hDist = getDist(xF - x0, yF - y0)
    vDist = heightArray[xF][yF] - heightArray[x0][y0]
    return math.e ** (3.5 * abs(vDist / hDist + 0.05))


def main(terrainFile, elevationFile, pathFile, season, outputFile):
    im = Image.open(terrainFile)
    pix = im.load()
    width, height = im.size

    for col in range(0, width):
        for row in range(0, height):
            color = pix[col, row][0:3]
            if color == (0, 0, 255):
                pix[col, row] = iceColor

    im.save(outputFile)


main('Inputs/mpTerrain.png', '', '', '', 'Outputs/out.png')
