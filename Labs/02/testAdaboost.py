from includes.adaTree import adaTree
from includes.readData import readExampleData


def main():
    dataSet, attrs, attrRanges, categories = readExampleData('Data/andExample.data')
    if len(categories) != 2:
        exit(1)

    ada = adaTree(dataSet, categories[0], categories[1], attrs, attrRanges, 3)

    for i in range(0, len(dataSet)):
        testCat, testDict = dataSet[i]
        if testCat != ada.eval(testDict):
            print('Missed ' + str(i))

    return


if __name__ == '__main__':
    main()
