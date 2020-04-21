from includes.dTree import dTree, weightedDTree
from includes.readData import readExampleData


def main():
    dataSet, attrs, attrRanges, categories = readExampleData('Data/andExample.data')
    wTree = weightedDTree()

    weight = float(1) / (len(dataSet))
    weights = []
    for datum in dataSet:
        weights.append(weight)

    wTree.teachWeighted(dataSet, weights, attrs, attrRanges, categories)

    tree = dTree()
    tree.teach(dataSet, attrs, attrRanges, categories)

    true = 'True'
    false = 'False'
    vals = [true, false]

    for i in range(0, len(dataSet)):
        testCat, testDict = dataSet[i]
        if testCat != wTree.eval(testDict):
            print(i)

    wTree.beautify()


for itt in range(0, 1):
    main()
