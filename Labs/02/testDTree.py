from includes.dTree import dTree, weightedDTree
from includes.readData import readData

import pickle


def main():
    dataSet, attrs, attrRanges, categories = readData('Data/classExample.data')
    wTree = weightedDTree()

    weight = float(1) / len(dataSet)
    weights = []
    for datum in dataSet:
        weights.append(weight)

    wTree.teachWeighted(dataSet, weights, attrs, attrRanges, categories)

    tree = dTree()
    tree.teach(dataSet, attrs, attrRanges, categories)

    true = 'True'
    false = 'False'
    vals = [true, false]

    for hornVal in vals:
        for fluteVal in vals:
            for guitarVal in vals:
                testDict = {'Horn': hornVal, 'Flute': fluteVal, 'Guitar': guitarVal}
                if wTree.eval(testDict) != tree.eval(testDict):
                    print('\terror on ' + str(testDict))
                    return
                print('\t' + str(testDict) + ' -> ' + tree.eval(testDict))


for i in range(0, 1000):
    print('Attempt ' + str(i) + ':')
    main()
