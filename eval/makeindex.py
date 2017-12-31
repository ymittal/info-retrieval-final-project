
import os
import sys

def printUsageAndExit():
    args = " input_file"
    print("Usage: " + sys.argv[0] + args, file=sys.stderr)
    sys.exit(1)

def loadIds(filename):
    ids = []
    readId = False
    with open (filename) as f:
        for line in f:
            line = line.strip()
            if readId:
                ids.append(line)
                readId = False
            elif line.startswith('<DOCNO>'):
                # ID is on next line
                readId = True
    ids.sort()
    return ids

def writeIds(filename, ids):
    ext = os.path.basename(filename).rpartition(".")[2]
    with open('idx.{}'.format(ext), 'w+') as f:
        for id in ids:
            print(id, file=f)

def main():
    if len(sys.argv) < 2:
        printUsageAndExit()
    inputfilename = sys.argv[1]
    ids = loadIds(inputfilename)
    writeIds(inputfilename, ids)

if __name__ == "__main__":
    # execute only if run as a script
    main()
