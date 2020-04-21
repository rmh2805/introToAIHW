import pickle
import sys
from includes.dTree import dTree
from includes.adaTree import adaTree


# Sets the default number of hypotheses for adaboost
def defaultAdaboostK():
    return 5


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
        print('usage: train(<exampleFile>, <hypothesisFile>, <"ada"|"dt"> [, <maxDepth>])')
        return

    isAda = learningType == 'ada'
    if isAda and maxDepth == -1:
        maxDepth = defaultAdaboostK()  # maxDepth handling for adaboost


def predict(hypothesisFile, dataFile):
    pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)
