import pickle
import sys
from includes.dTree import dTree
from includes.adaTree import adaTree
from includes.readData import readLangFile
from includes.attribute import attrSample, attribute

# Define the set of attributes to scan on
attrDef = [('s aa', 'substring', 'aa'),
           ('w the', 'word', 'the'),
           ('w de', 'word', 'de'),
           ('s ee', 'substring', 'ee'),
           ('w het', 'word', 'het'),
           ('w and', 'word', 'and'),
           ('w of', 'word', 'of'),
           ('s v', 'substring', 'v'),
           ('w door', 'word', 'w'),
           ('s oo', 'substring', 'oo')]

attrSet = set()
attrRanges = dict()
for tpl in attrDef:
    key = tpl[0]
    attrRanges[key] = {True, False}
    attrSet.add(key)


# Sets the default number of hypotheses for adaboost
def defaultAdaboostK():
    return 30


# This function will train either a decision tree (learningType = "dt") or adaboost on decision stumps
# (learningType = "ada") hypothesis to distinguish between dutch and english using a file of labeled
# examples (exampleFile).
#
# The function of maxDepth changes between learning types, and defaults to -1. On a decision tree it will act as a
# proper depth limit, with at most maxDepth + 1 generations created (root node is at depth 0), and will generate until
# example consensus, exhaustion of examples, or exhaustion of attributes otherwise.
#
# On adaboost, maxDepth controls the number of sub-hypotheses generated, and its default behaviour is defined in the
# `defaultAdaboostK` function
def train(exampleFile, hypothesisFile, learningType, maxDepth=-1):
    if learningType != 'ada' and learningType != 'dt':
        printUsage()
        return

    isAda = learningType == 'ada'
    if isAda and maxDepth == -1:
        maxDepth = defaultAdaboostK()  # maxDepth handling for adaboost

    strSet = readLangFile(exampleFile)
    dataSet = attribute(strSet, attrDef)

    hypo = None
    if isAda:
        hypo = adaTree(dataSet, 'en', 'nl', attrSet, attrRanges, maxDepth)
    else:
        hypo = dTree()
        hypo.teach(dataSet, attrSet, attrRanges, ['en', 'nl'])

    oFile = open(hypothesisFile, 'wb')
    pickle.dump(hypo, oFile)
    oFile.close()


def printUsage():
    print('Usage: ' + sys.argv[0] + 'train <exampleFile> <hypothesisFile> <"ada"|"dt"> [maxDepth]')
    print('       -or-')
    print('       ' + sys.argv[0] + 'predict <hypothesisFile> <dataFile>')


def predict(hypothesisFile, dataFile):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2 or (sys.argv[1] != 'train' and sys.argv[1] != 'predict') or \
            (sys.argv[1] == 'train' and len(sys.argv) < 5) or \
            (sys.argv[1] == 'predict' and len(sys.argv < 4)):
        printUsage()
        exit(1)

        if len(sys.argv) == 5:
            train(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            train(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]))
    else:
        predict(sys.argv[2], sys.argv[3])
