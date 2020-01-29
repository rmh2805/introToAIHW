# Prompt the user for words to path between
def promptWords():
    w1 = input("     Enter your first word: ").strip()
    w2 = input("    Enter your second word: ").strip()

    if len(w1) == 0:
        w1 = "foo"

    if len(w2) == 0:
        w2 = "bar"

    return w1, w2


# Prompt the user for the path to a dictionary file
def promptDict():
    dictPath = input("Enter your dictionary path: ").strip()

    if len(dictPath) == 0:
        dictPath = "exampleWords.txt"

    return dictPath


# Turn the dictionary file into a list of legal words
def listWords(dictPath):
    dict_file = open(dictPath, "r")
    words = dict_file.readlines()
    dict_file.close()

    for i in range(0, len(words)):
        words[0] = words[0].strip()

    return words


# Counts the difference in characters between the two provided strings
def difChars(w1, w2):
    dif = abs(len(w1) - len(w2))
    for i in range(0, min(len(w1), len(w2))):
        if w1[i] != w2[i]:
            dif += 1

    return dif


# Gives a list of all possible next nodes (1 char changed from the word in)
def generateNodes(wordIn, words):
    actions = []
    for word in words:
        if difChars(wordIn, word) == 1:
            actions.append(word)

    return actions


def main():
    w1 = "small"
    w2 = "short"
    dictPath = "exampleWords.txt"
    words = listWords(dictPath)

    for i in range(0, len(words)):
        words[i] = words[i].strip()
    if w1 not in words:
        print("ERROR: " + w1 + " is not in the provided dictionary")
        return 1
    if w2 not in words:
        print("ERROR: " + w2 + " is not in the provided dictionary")
        return 1

    visited = findPath(w1, w2, words)
    return 0


class myNode:
    word = ""
    parent = ""
    g = 0
    f = 0

    def __init__(self, word="", parent="", g=0, f=0):
        self.word = word
        self.parent = parent
        self.g = g
        self.f = f


# Best first search
def findPath(w1, w2, words):
    visited = {}

    # Create a node for the starting point
    myNode(w1, "", 0, difChars(w1, w2))
    toVisit = [myNode]

    return visited


if __name__ == '__main__':
    exit(main())
