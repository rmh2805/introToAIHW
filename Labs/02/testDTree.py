from includes.dTree import dTree, adaTree
from includes.readData import readData


def main():
    dataSet, attrs, attrRanges, categories = readData('Data/classExample.data')
    tree = dTree()
    tree.teach(dataSet, attrs, attrRanges, categories)

    true = 'True'
    false = 'False'
    testDict = {'Horn': false, 'Flute': true, 'Guitar': false}
    print(tree.eval(testDict))


main()
