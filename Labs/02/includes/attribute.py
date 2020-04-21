def hasWord(text, word):
    return word.lower() in text.lower().split()


def hasSubstring(text, substring):
    return substring.lower() in text.lower()


def attrSample(sample, attrDef):
    return attribute([sample], attrDef)[0]


def attribute(data, attrDef):

    attrList = list()
    for datum in data:
        category, text = datum
        attrs = dict()

        for attrSet in attrDef:
            attr, kind, key = attrSet

            if kind == 'word':
                attrs[attr] = hasWord(text, key)
            elif kind == 'substring':
                attrs[attr] = hasSubstring(text, key)
            elif kind == 'misc':
                attrs[attr] = key(text)
            else:
                print('Error: Attribution function was passed an unrecognized class of attribute (' + kind + ')')
                exit(1)

        attrList.append((category, attrs))

    return attrList
