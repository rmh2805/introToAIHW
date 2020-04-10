from math import log2


def countCategories(tSet, categories):
    count = dict()
    for category in categories:
        count[category] = 0

    for datum in tSet:
        count[datum[0]] += 1

    return count


class dTree:
    def __init__(self):
        self.nodes = dict()
        self.categories = None
        self.attributes = None

        self.nodeCount = 0

    @classmethod
    def maxKey(cls, count):
        maxCat = None
        for category in count:
            if maxCat is None:
                maxCat = category

            if count[category] > count[maxCat]:
                maxCat = category

        return maxCat

    @staticmethod
    def unanimousTSet(tSet):
        tSet = list(tSet)
        if len(tSet) == 0:
            return False  # Fail out (potentially different behaviour) on empty tSet

        category = tSet[0][0]  # Category of the first element in the tSet
        for datum in tSet:
            if datum[0] != category:
                return False  # If any category doesn't match the first, not unanimous
        return True  # If all categories match the first, unanimous

    @staticmethod
    def splitAttr(tSet, attr, attrRange):
        split = dict()
        for val in attrRange:
            split[val] = list()

        for datum in tSet:
            split[datum[1][attr]].append(datum)

        return split

    @classmethod
    def setEntropy(cls, tSet, categories):
        subsetSize = len(tSet)
        if subsetSize == 0:
            return -1  # Exit before dividing by zero

        count = countCategories(tSet, categories)

        total = 0
        for category in categories:
            if count[category] == 0:
                continue

            p = count[category] / subsetSize  # Get proportion of this category
            total += p * log2(p)  # Calculate category information in bits
        return -total

    @classmethod
    def getMajority(cls, tSet, categories):
        return cls.maxKey(countCategories(tSet, categories))

    @classmethod
    def maxAttr(cls, tSet, attrSet, attrRanges, categories):
        base = cls.setEntropy(tSet, categories)

        bestAttr = None
        bestSplit = None
        bestInfoGain = None
        for attr in attrSet:
            split = cls.splitAttr(tSet, attr, attrRanges[attr])

            remainder = 0.0
            for val in split:
                remainder += len(split[val]) / len(tSet) * cls.setEntropy(split[val], categories)

            infoGain = base - remainder
            if bestInfoGain is not None and bestInfoGain > infoGain:
                continue

            bestAttr = attr
            bestSplit = split
            bestInfoGain = infoGain

        return bestAttr, bestSplit

    def teach(self, tSet, attrSet, attrRanges, categories, parent=None):
        # ==========================================<Handle Inputs>=========================================== #
        if parent is None:  # At the root of the tree, record categories and attrs
            self.categories = categories
            self.attributes = attrSet

        tSet = list(tSet)
        attrSet = set(attrSet).copy()

        # ======================================<Initialize a New Node>======================================= #
        uid = self.nodeCount
        self.nodeCount += 1

        nodeDict = dict()
        self.nodes[uid] = nodeDict  # Create a new node

        nodeDict['parent'] = parent
        nodeDict['isLeaf'] = False  # Default to a non-leaf node

        if len(tSet) == 0:
            nodeDict['isLeaf'] = True  # Nothing to train on, must be a leaf
            nodeDict['bias'] = self.nodes[parent]['bias']  # Nothing to train on, default to parent
            return  # This branch is terminated

        # This node is biased towards tSet's plurality category
        nodeDict['bias'] = self.getMajority(tSet, categories)

        if len(attrSet) == 0:
            nodeDict['isLeaf'] = True  # Nothing to split on, can't branch further
            return  # This branch is terminated

        if self.unanimousTSet(tSet):
            nodeDict['isLeaf'] = True  # No need to split further, all in agreement here
            return  # This branch is terminated

        # ==========================================<Make Children>=========================================== #
        attr, split = self.maxAttr(tSet, attrSet, attrRanges, categories)
        nodeDict['attr'] = attr
        nodeDict['children'] = dict()

        attrSet.remove(attr)  # Can no longer split on this attr
        for val in attrRanges[attr]:
            nodeDict['children'][val] = self.nodeCount  # The next child made will be my child from this node
            self.teach(split[val], attrSet, attrRanges, categories, uid)  # Train a new child after splitting on attr

    def beautify(self, node=0, depth=0):
        if depth == 0:
            print('+ ', end='')

        nodeDict = self.nodes[node]

        if nodeDict['isLeaf']:
            print(nodeDict['bias'])
            return

        print(nodeDict['attr'])

        depth += 1
        for val in nodeDict['children']:
            for i in range(0, depth):
                print('|', end='')
            print('+ ', end='')
            print(str(val) + ': ', end='')
            self.beautify(nodeDict['children'][val], depth)

    def eval(self, attrs):
        node = 0
        nodeDict = self.nodes[node]

        while not nodeDict['isLeaf']:
            val = attrs[nodeDict['attr']]
            node = nodeDict['children'][val]
            nodeDict = self.nodes[node]

        return nodeDict['bias']

    def __str__(self):
        return '<dTree: ' + str(self.attributes) + '->' + str(self.categories) + '>'


class weightedDTree(dTree):
    def __init__(self):
        super(weightedDTree, self).__init__()

    def teachWeighted(self, tSet, weights, attrSet, attrRanges, categories):
        if len(weights) < len(tSet):
            return False

        tSet = list(tSet)
        wTSet = list()
        for i in range(0, len(weights)):
            wTSet.append((tSet[i][0], tSet[i][1], weights[i]))

        self.teach(wTSet, attrSet, attrRanges, categories)
        return True

    @classmethod
    def setEntropy(cls, tSet, categories):
        if len(tSet) == 0:
            return -1

        sums = cls.categoryWeights(tSet, categories)

        total = 0.0
        for category in categories:
            if sums[category] == 0:
                continue
            total += sums[category] * log2(sums[category])

        return -total

    @classmethod
    def categoryWeights(cls, tSet, categories):
        sums = dict()
        for category in categories:
            sums[category] = 0.0

        for datum in tSet:
            sums[datum[0]] += datum[2]

        return sums

    @classmethod
    def maxAttr(cls, tSet, attrSet, attrRanges, categories):
        base = cls.setEntropy(tSet, categories)

        bestAttr = None
        bestSplit = None
        bestInfoGain = None
        for attr in attrSet:
            split = cls.splitAttr(tSet, attr, attrRanges[attr])

            remainder = 0.0
            for val in split:
                valWeight = 0.0
                for datum in split[val]:
                    valWeight += datum[2]
                remainder += valWeight * cls.setEntropy(split[val], categories)

            infoGain = base - remainder
            if bestInfoGain is not None and bestInfoGain > infoGain:
                continue

            bestAttr = attr
            bestSplit = split
            bestInfoGain = infoGain

        return bestAttr, bestSplit

    @classmethod
    def getMajority(cls, tSet, categories):
        return cls.maxKey(cls.categoryWeights(tSet, categories))

    def __str__(self):
        return '<weightedDTree: ' + str(self.attributes) + '->' + str(self.categories) + '>'
