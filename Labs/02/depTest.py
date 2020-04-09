from includes.depTree import dNode
from includes.readData import readData


def testCreation(trainingDataFile):
    dataSet, attrs, attrRanges, categories = readData(trainingDataFile)
    baseNode = dNode()
    baseNode.train(dataSet, attrs, attrRanges, categories, None)
    return baseNode


def testEval(baseNode, testData):
    print(baseNode.eval(testData))


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


def main():
    baseNode = testCreation('classExample.data')
    baseAttrs = {'Horn': 'True', 'Flute': 'False', 'Guitar': 'False'}
    baseNode.encode('baseTree.data')
    baseNode = dNode.decode('baseTree.data')
    print(baseNode.eval(baseAttrs))
    pTree(baseNode)


if __name__ == '__main__':
    main()
