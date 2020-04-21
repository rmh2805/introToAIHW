from .dTree import weightedDTree
from math import log


class adaTree:
    @classmethod
    def threshold(cls, x):
        if x < 0:
            return -1
        return 1

    @staticmethod
    def normalizeWeights(weights):
        f = sum(weights)
        for i in range(0, len(weights)):
            weights[i] = weights[i] / f

    def __init__(self, tSet, posCat, negCat, attrSet, attrRanges, numHypotheses=1):
        self.hypotheses = list()
        self.hypoWeights = list()
        self.posCat = posCat
        self.negCat = negCat

        # Create a list for sample weights and initialize with equal weighting
        weights = list()
        for i in range(0, len(tSet)):
            weights.append(1.0 / len(tSet))

        categories = [posCat, negCat]
        for hypo in range(0, numHypotheses):  # Generate N hypotheses
            wTree = weightedDTree()
            wTree.teachWeighted(tSet, weights, attrSet, attrRanges, categories, 1)  # Generate a new decision stump
            self.hypotheses.append(wTree)  # Add this decision stump to the list of hypotheses

            # Separate the caught and missed inputs to the new stump
            caught = list()
            missed = list()
            for i in range(0, len(tSet)):
                cat, attrs = tSet[i]
                result = wTree.eval(attrs)
                if cat == result:
                    caught.append(i)
                else:
                    missed.append(i)

            # Calculate the error (sum of missed weights)
            error = 0.0
            for val in missed:
                error += weights[val]

            adj = error / (1 - error)  # Calculate new weight for correct samples
            self.hypoWeights.append(log((1 - error) / error))  # Assign a hypothesis weight

            # Adjust the weights of the correct samples
            for val in caught:
                weights[val] *= adj

            self.normalizeWeights(weights)

    def eval(self, attrs):
        tot = 0.0
        for i in range(0, len(self.hypotheses)):
            result = self.hypotheses[i].eval(attrs)
            weight = self.hypoWeights[i]
            if result == self.negCat:
                tot -= weight
            else:
                tot += weight

        if self.threshold(tot) == 1:
            return self.posCat
        return self.negCat
