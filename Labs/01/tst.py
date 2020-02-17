import math

from PIL import Image


# im = Image.open("Inputs/mpTerrain.png")
def pace(slope):
    return math.e**(3.5 * abs(slope + 0.05))


def time(slope, dist):
    return pace(slope) * dist


def pathTime(pathIn):
    duration = 0
    for step in pathIn:
        duration += time(step, 1)
    return duration


horiDist = 100
vertDist = 0
slopes = [0, 1/20, 1, 5, 10, 20, 30, 45, 90]
for mySlope in slopes[1:]:
    slopes.append(-mySlope)


overallTime = time(vertDist/horiDist, horiDist)


def makePath(avgTime, depth, dH=0, timeAcc=0):
    if depth == 1:
        return timeAcc + time(dH, 1)

    if timeAcc > avgTime:
        return timeAcc + avgTime

    for slopeI in slopes:
        duration = makePath(avgTime, depth - 1, dH + slopeI, timeAcc + pace(slopeI))
        if duration < avgTime:
            return duration
    return timeAcc + avgTime


print(overallTime)
print(makePath(overallTime, horiDist))
