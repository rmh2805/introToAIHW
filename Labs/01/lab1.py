import sys

from PIL import Image

terrainImage = None

terrainData = None
mapWidth = 0
mapHeight = 0


def putColor(row, col, color):
    terrainData[col, row] = color


def getColor(row, col):
    return terrainData[col, row]


def writeImage(outputFile):
    global terrainImage
    terrainImage.save(outputFile)


def initializeTerrain(terrainFile):
    global terrainImage
    global terrainData
    terrainImage = Image.open(terrainFile)
    terrainData = terrainImage.load()


def main(terrainFile, elevationFile, pathFile, season, outputFile):
    initializeTerrain(terrainFile)

    for row in range(0, 10):
        for col in range(20, 30):
            putColor(row, col, (0xFF, 0xFF, 0x00))

    writeImage(outputFile)


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if argc != 6:
        print('Usage: python3 ' + argv[0] + ' <Terrain File> <Elevation File> <Path File> <Season> <Output File>')
        exit(1)

    main(argv[1], argv[2], argv[3], argv[4], argv[5])
