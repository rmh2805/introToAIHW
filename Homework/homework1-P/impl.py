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
    if isinstance(w1, myNode):
        w1 = w1.word

    if isinstance(w2, myNode):
        w2 = w2.word

    dif = abs(len(w1) - len(w2))
    for i in range(0, min(len(w1), len(w2))):
        if w1[i] != w2[i]:
            dif += 1

    return dif


# Gives a list of all possible next nodes (1 char changed from the word in)
def getActions(wordIn, words):
    if isinstance(wordIn, myNode):
        wordIn = wordIn.word

    actions = []
    for word in words:
        if difChars(wordIn, word) == 1:
            actions.append(word)

    return actions


def main():
    (w1, w2) = promptWords()
    dictPath = promptDict()
    words = listWords(dictPath)

    for i in range(0, len(words)):
        words[i] = words[i].strip()
    if w1 not in words:
        print("ERROR: " + w1 + " is not in the provided dictionary")
        return 1
    if w2 not in words:
        print("ERROR: " + w2 + " is not in the provided dictionary")
        return 1

    path = findPath(w1, w2, words)
    print(path)
    return 0


class myNode:
    word = ""
    parent = ""
    g = 0

    def __init__(self, word="", parent="", g=0):
        self.word = word
        self.parent = parent
        self.g = g

    def __eq__(self, other):
        if isinstance(other, str):
            return self.word == other
        if isinstance(other, self.__class__):
            return self.word == other.word
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def makePath(visitedMap, dest):
    path = []
    word = dest
    while word != "":
        path.insert(0, word)
        word = visitedMap[word].parent

    return path


# Best first search
def findPath(start, dest, words):
    # Create a node for the starting point (no parent, no path weight)
    sNode = myNode(start)

    # Mark the
    pQueue = [sNode]
    visited = {start: sNode}

    while len(pQueue) > 0:
        node = pQueue.pop(0)

        # If the lowest weighted node is our destination, we have found a shortest path
        if node == dest:
            return makePath(visited, dest)

        # Get potential next words from `node`'s word
        # noinspection PyTypeChecker
        actions = getActions(node, words)

        for action in actions:
            """ If this action has already been taken:
                    grab the node generated for it then and then skip to the next action if this route is faster
                If this is a new action:
                    generate a new node for this action and mark it as visited
            """
            if action in visited:
                aNode = visited[action]
                if aNode.g <= node.g + 1:
                    continue
            else:
                aNode = myNode(action)
                visited[action] = aNode

            # Since this is the fastest known path to aNode, update its path cost and parent
            aNode.g = node.g + 1
            aNode.parent = node.word

            # Enqueue this node if it is not already in queue
            if aNode not in pQueue:
                pQueue.append(aNode)

        pQueue.sort(key=lambda n: n.g + difChars(n, dest))  # Sort the list by pathCost + heuristic

    # Failed to find a route
    return "Failure"


if __name__ == '__main__':
    exit(main())
