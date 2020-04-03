from math import log2


# =========================================<File IO>================================================================== #
def readData(filePath):
    fp = open(filePath, 'r')
    topLine = fp.readline().strip()
    data = topLine.split(':')

    attrs = data[0].split(',')
    attrRanges = dict()
    for i in range(0, len(attrs)):
        attrs[i] = attrs[i].strip()
        attrRanges[attrs[i]] = set()

    categories = data[1].split(',')
    for i in range(0, len(categories)):
        categories[i] = categories[i].strip()

    dataSet = []
    lines = fp.readlines()
    for line in lines:
        data = line.split(':')
        category = data[1].strip()

        data = data[0].split(',')
        attrVals = dict()
        for i in range(0, len(data)):
            attr = attrs[i]
            attrVal = data[i].strip()
            attrVals[attr] = attrVal
            if attrVal not in attrRanges[attr]:
                attrRanges[attr].add(attrVal)
        dataSet.append((category, attrVals))

    fp.close()

    return dataSet, attrs, attrRanges, categories


# =========================================<Set Operations>=========================================================== #
def countCategories(dataSet, categories):
    count = dict()
    for category in categories:
        count[category] = 0
    for data in dataSet:
        count[data[0]] += 1
    return count


def splitAttribute(dataSet, attribute, attributeRange):
    split = dict()
    for attributeR in attributeRange:
        split[attributeR] = list()

    for data in dataSet:
        split[data[1][attribute]].append(data)

    return split


def maxCategory(dataSet, categories):
    count = countCategories(dataSet, categories)

    maxCat = None
    for category in count:
        if maxCat is None:
            maxCat = category
        elif count[category] > count[maxCat]:
            maxCat = category
    return maxCat


def united(dataSet):
    if len(dataSet) == 0:
        return True

    category = None
    for data in dataSet:
        if category is None:
            category = data[0]
        elif data[0] != category:
            return False
    return True


# =========================================<Information Evaluation>=================================================== #
def subsetEntropy(subset, categories):
    subsetSize = len(subset)
    count = countCategories(subset, categories)
    if united(subset):
        return 0

    total = 0
    for category in categories:
        p = count[category] / subsetSize
        if p == 0:
            continue
        total += p * log2(p)
    return -total


# Returns the information gained by splitting on attr, followed by a map with split performed (save the work)
def attrInfoGain(dataSet, attr, attrRange, categories):
    split = splitAttribute(dataSet, attr, attrRange)

    total = 0.0
    for attrVal in attrRange:
        temp = subsetEntropy(split[attrVal], categories)
        total += temp * len(split[attrVal]) / len(dataSet)
    return subsetEntropy(dataSet, categories) - total, split


def decisionTreeLearning(examples, attrs, parentSet, categories):
    if len(examples) == 0:
        return maxCategory(parentSet)
    elif united(examples, categories):
        pass


class dNode:
    def __init__(self, trainingSet, attrSet, attrRanges, categories, parent):
        attrSet = set(attrSet).copy()
        categories = list(categories)

        self.attr = None
        self.bias = None
        self.children = dict()
        self.isLeaf = True

        if len(trainingSet) == 0 and parent is not None:
            self.bias = parent.bias
        elif len(trainingSet) == 0:
            self.bias = categories[0]
        else:
            self.bias = maxCategory(trainingSet, categories)

        if len(attrSet) == 0 or len(trainingSet) == 0 or united(trainingSet):
            self.isLeaf = True
            return
        self.isLeaf = False

        bestAttr = None
        bestSplit = None
        bestInfo = None
        for attr in attrSet:
            info, split = attrInfoGain(trainingSet, attr, attrRanges[attr], categories)

            if bestAttr is not None and info <= bestInfo:
                continue

            bestAttr = attr
            bestSplit = split
            bestInfo = info

        self.attr = bestAttr
        attrSet.remove(self.attr)
        for attrVal in attrRanges[self.attr]:
            self.children[attrVal] = dNode(bestSplit[attrVal], attrSet, attrRanges, categories, self)


def main():
    dataSet, attrs, attrRanges, categories = readData('classExample.data')
    baseNode = dNode(dataSet, attrs, attrRanges, categories, None)
    pTree(baseNode)


def treeBranch(depth):
    for i in range(0, depth - 1):
        print('|', end='')
    print('+', end='')


def pTree(node, depth=1):
    if depth == 1:
        print('+Base: ', end='')
    if not node.isLeaf:
        print(node.attr)
    else:
        print(node.bias)
    depth += 1
    for childVal in node.children:
        treeBranch(depth)
        print(str(childVal) + ': ', end='')
        pTree(node.children[childVal], depth)


if __name__ == '__main__':
    main()
