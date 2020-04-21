import sys


def main():
    if len(sys.argv) < 3:
        exit(1)

    fIn = open(sys.argv[1], 'r', encoding='utf8')
    lines = fIn.readlines()
    fIn.close()

    fOut = open(sys.argv[2], 'w', encoding='utf8')
    for line in lines:
        fOut.write(line.split('|')[1])
    fOut.close()


if __name__ == '__main__':
    main()
