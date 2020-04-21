from includes.readData import readLangFile
from includes.attribute import attribute, attrSample

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

attrRanges = dict()
for tpl in attrDef:
    key = tpl[0]
    attrRanges[key] = {True, False}


def main():
    data = readLangFile('ExampleFiles/20.data')
    dataSet = attribute(data, attrDef)

    for i in range(0, len(data)):
        print(dataSet[i])

    print()
    print(attrRanges)
    print(len(attrRanges))

    print(attrSample(('en', 'Yeah sex is good and all, but have you ever tried garlic bread? Shit\'s tops!'), attrDef))


if __name__ == '__main__':
    main()
