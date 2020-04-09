def readData(filePath):
    fp = open(filePath, 'r')
    topLine = fp.readline().strip()
    data = topLine.split(':')

    attrs = data[0].split(',')
    attrRanges = dict()
    for i in range(0, len(attrs)):
        attrs[i] = attrs[i].strip()
        attrRanges[attrs[i]] = set()

    categories = data[1].split(',')
    for i in range(0, len(categories)):
        categories[i] = categories[i].strip()

    dataSet = []
    lines = fp.readlines()
    for line in lines:
        data = line.split(':')
        category = data[1].strip()

        data = data[0].split(',')
        attrVals = dict()
        for i in range(0, len(data)):
            attr = attrs[i]
            attrVal = data[i].strip()
            attrVals[attr] = attrVal
            if attrVal not in attrRanges[attr]:
                attrRanges[attr].add(attrVal)
        dataSet.append((category, attrVals))

    fp.close()

    return dataSet, attrs, attrRanges, categories
