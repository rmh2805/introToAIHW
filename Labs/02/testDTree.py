from includes.dTree import dTree, weightedDTree
from includes.readData import readData

import pickle


def main():
    dataSet, attrs, attrRanges, categories = readData('Data/classExample.data')
    tree = weightedDTree()

    weight = float(1)/len(dataSet)
    weights = []
    for datum in dataSet:
        weights.append(weight)

    tree.teachWeighted(dataSet, weights, attrs, attrRanges, categories)

    true = 'True'
    false = 'False'
    testDict = {'Horn': false, 'Flute': true, 'Guitar': false}

    print(tree.eval(testDict))


main()
