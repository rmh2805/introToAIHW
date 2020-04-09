from math import log2


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


dNodeID = 0


def getDNodeID():
    global dNodeID
    temp = dNodeID
    dNodeID += 1
    return temp


class dNode:
    dNodeEncodingHeader = 'dNodeEncoding\n'

    def __init__(self, uid=None):
        global dNodeID

        self.attr = None
        self.bias = None
        self.children = dict()
        self.isLeaf = True
        if uid is None:
            self.uid = getDNodeID()
        else:
            self.uid = uid

    def train(self, trainingSet, attrSet, attrRanges, categories, parent):
        attrSet = set(attrSet).copy()
        categories = list(categories)
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
            self.children[attrVal] = dNode()
            self.children[attrVal].train(bestSplit[attrVal], attrSet, attrRanges, categories, self)

    def parseDict(self, paramDict):
        self.uid = paramDict['uid']
        self.attr = paramDict['attr']
        self.bias = paramDict['bias']
        self.isLeaf = paramDict['isLeaf']

        self.children = dict()
        if len(paramDict['children'].strip()) == 0:
            return

        for group in paramDict['children'].split('..'):
            group = group.split(';')
            self.children[group[0].strip()] = int(group[1].strip())

    def eval(self, attrMap):
        if self.isLeaf:
            return self.bias
        else:
            return self.children[attrMap[self.attr]].eval(attrMap)

    def encode(self, fileName):
        fp = open(fileName, 'w')
        fp.write(dNode.dNodeEncodingHeader)
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)
            fp.write(str(node) + '\n')

            if node.isLeaf:
                continue

            for attrVal in node.children:
                queue.append(node.children[attrVal])

        fp.close()

    @staticmethod
    def decode(fileName):
        fp = open(fileName, 'r')
        if fp.readline().strip() != dNode.dNodeEncodingHeader.strip():
            fp.close()
            return None

        data = fp.readlines()
        dicts = []
        fp.close()

        for i in range(0, len(data)):
            datum = data[i].strip()[1:-1].split(',')
            fieldDict = dict()
            for field in datum:
                field = field.strip().split(':')
                fieldDict[field[0].strip()] = field[1].strip()

            if fieldDict['type'] != "dNode":
                continue
            dicts.append(fieldDict)
            fieldDict['uid'] = int(fieldDict['uid'])
            fieldDict['isLeaf'] = fieldDict['isLeaf'] == 'True'
            fieldDict['children'] = fieldDict['children'][1:-1]

            if fieldDict['attr'] == 'None':
                fieldDict['attr'] = None

        baseNode = None
        nodeDict = dict()
        for i in range(0, len(dicts)):
            paramDict = dicts[i]
            nodeUID = paramDict['uid']
            node = dNode()
            if i == 0:
                baseNode = node

            nodeDict[nodeUID] = node

            node.parseDict(paramDict)

        for uid in nodeDict:
            node = nodeDict[uid]
            for child in node.children:
                node.children[child] = nodeDict[node.children[child]]

        return baseNode

    def __str__(self):
        st = '{type:dNode'
        st += ', uid:' + str(self.uid)
        st += ', bias:' + str(self.bias)
        st += ', attr:' + str(self.attr)
        st += ', isLeaf:' + str(self.isLeaf)
        st += ', children:{'
        for attrVal in self.children:
            if st[-1] != '{':
                st += '..'
            st += str(attrVal) + ';' + str(self.children[attrVal].uid)

        st += '}}'
        return st
