import math

from PIL import Image

# im = Image.open("Inputs/mpTerrain.png")

horiDist = 1000
vertDist = 0

rawSlope = vertDist/horiDist
overallPace = math.e**(3.5 * abs(rawSlope + 0.05))

print(overallPace)

slopes = [0, 1/20, 1, 5, 10, 20, 30, 45, 90]


for slope in slopes[1:]:
    slopes.append(-slope)



for dHori in range(0, 1000):
    pass

print(slopes)
