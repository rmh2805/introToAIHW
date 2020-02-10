import math
import random
import time


# ================================================<String Generation>================================================= #

#   Leftover wrapper, here to give a default constant seed if needed (for number set generation
def setSeed(seed):
    random.seed(seed)


#   Called once to generate a fixed list and target then set seed to time
def makeNums(n):
    setSeed(127000000001)

    nums = []
    for i in range(0, n):
        nums.append(random.randint(0, 9))

    tgt = random.randint(0, pow(10, int(math.log(n, 10)) + 2) - 1)

    setSeed(int(time.time()))
    return nums, tgt


#   Generate a legal list of operations on this numList (no /0 errors)
def makeOps(numList):
    # 0: add, 1: subtract, 2: multiply, 3: divide
    ops = []
    for i in range(0, len(numList) - 1):
        if numList[i + 1] == 0:  # No divide by zero
            ops.append(random.randint(0, 2))
        else:
            ops.append(random.randint(0, 3))
    return ops


#   Shuffle the number list and return a random list of ops on them
def restart(numList):
    random.shuffle(numList)
    return makeOps(numList)


# ==================================================<String Parsing>================================================== #

#   Turns an operator index into a character
def op2Char(op):
    if op == 0:
        return '+'
    elif op == 1:
        return '-'
    elif op == 2:
        return '*'
    else:
        return '/'


#   Makes a printable string from the provided lists of numbers and ops
def makeStr(numList, opsList):
    st = ''

    for i in range(0, len(opsList)):
        st += str(numList[i]) + ' ' + op2Char(opsList[i]) + ' '
    st += str(numList[-1])

    return st


#   Evaluates the numbers by the ops from left to right
def evalStr(numList, opsList):
    acc = numList[0]
    for i in range(0, len(opsList)):
        num = numList[i + 1]
        op = opsList[i]
        if op == 0:
            acc += num
        elif op == 1:
            acc -= num
        elif op == 2:
            acc *= num
        else:
            acc /= num
    return acc


# ================================================<String Operations>================================================= #

#   Swap the positions of the numbers at indexes a and b in numList (return None if illegal, new numList if legal)
def swap(numList, opsList, a, b):
    numList = numList.copy()
    if a >= len(numList) or b >= len(numList):
        return None

    # if either is a second operand, its opposite is a zero, and the operator before it is a divide, return None
    if (a != 0 and numList[b] == 0 and opsList[a - 1] == 3) or \
            (b != 0 and numList[a] == 0 and opsList[b - 1] == 3):
        return None

    tmp = numList[a]
    numList[a] = numList[b]
    numList[b] = tmp
    return numList


#   Change the operand between numbers a and a+1 to new index op (return None if no change or illegal, new opsList else)
def change(numList, opsList, a, op):
    # Index in range or no change check
    if a >= len(opsList) or opsList[a] == op:
        return None

    # Divide by zero check
    if op == 3 and numList[a + 1] == 0:
        return None

    opsList = opsList.copy()
    opsList[a] = op
    return opsList


# =================================================<Search Function>================================================== #
bestState = None


#   Evaluate the results of all actions from current state and return the best (None if no better neighbor)
def lowestNeighbor(current, tgt):
    bestDiff = current[0]
    numList = current[1]
    opsList = current[2]

    minAct = None

    # Iterate through all possible swaps
    for i in range(0, len(numList) - 1):
        for j in range(i, len(numList)):
            newNumList = swap(numList, opsList, i, j)
            if newNumList is None:
                continue

            newDiff = getDiff(newNumList, opsList, tgt)
            if newDiff < bestDiff:
                bestDiff = newDiff
                minAct = ('s', i, j, newDiff)

    # Iterate through all possible changes
    for i in range(0, len(opsList)):
        for op in range(0, 4):
            newOpsList = change(numList, opsList, i, op)
            if newOpsList is None:
                continue

            newDiff = getDiff(numList, newOpsList, tgt)
            if newDiff < bestDiff:
                bestDiff = newDiff
                minAct = ('c', i, op, newDiff)

    return minAct


#   Objective function (minimize), keeps bestState up to date with best discovered state
def getDiff(numList, opsList, tgt):
    diff = abs(evalStr(numList, opsList) - tgt)

    global bestState
    if bestState is None or diff < bestState[0]:
        bestState = (diff, numList.copy(), opsList.copy())

    return diff


#   Makes a standard tuple from current state: (diff, numList, opsList)
def makeNode(numList, opsList, tgt):
    return getDiff(numList, opsList, tgt), numList, opsList


#   Generate a new node based on the current node and the given action
def takeAction(current, action):
    numList = current[1]
    opsList = current[2]

    if action[0] == 'c':
        opsList = change(numList, opsList, action[1], action[2])
    else:
        numList = swap(numList, opsList, action[1], action[2])

    return action[-1], numList, opsList


#   Generate a new start state and find a local minimum (returns local min state `(diff, numList, opsList)`)
def hillClimb(numList, tgt):
    numList = numList.copy()
    opsList = restart(numList)
    current = makeNode(numList, opsList, tgt)
    print('\ts0: ' + node2String(current) + '\n')

    while True:
        if current[0] == bestState[0]:
            print('\n\tBest State: ' + node2String(current))

        neighbor = lowestNeighbor(current, tgt)
        if neighbor is None:
            return current

        current = takeAction(current, neighbor)


def node2String(node):
    if node is None:
        return "None"
    return makeStr(node[1], node[2]) + '\n\tDistance to Target: ' + str(node[0])


#   Random restart hill climb implementation
def rrHillClimb(numList, tgt):
    startTime = time.time()
    iteration = 1
    while True:
        print('**************************************************************')
        print('RR Iteration: ' + str(iteration))
        if bestState is not None:
            print('Overall Best: ' + str(bestState[0]))

        hillClimb(numList, tgt)

        if bestState[0] == 0:
            return time.time() - startTime

        iteration += 1


# =================================================<Main Executable>================================================== #
def main(n):
    global bestState

    nums, tgt = makeNums(n)
    print('Number Set: ', end='')
    print(nums)
    print('Target Value: ' + str(tgt))

    acc = []
    for i in range(0, 100):
        bestState = None
        acc.append(rrHillClimb(nums, tgt))

    print('avg time: ' + str(math.fsum(acc) / 100) + ' seconds')


main(100)
