
import sys

def printUsageAndExit():
    args = " input_file"
    print("Usage: " + sys.argv[0] + args, file=sys.stderr)
    sys.exit(1)

def convertDocs(filename):
    with open (filename) as f:
        for line in f:
            line = line[:-1]
            line = line.replace('<DOC>', '<doc>')
            line = line.replace('</DOC>', '</doc>')
            line = line.replace('<DOCNO>', '<field name="id">')
            line = line.replace('</DOCNO>', '</field>')
            line = line.replace('<LINK>', '<field name="link">')
            line = line.replace('</LINK>', '</field>')
            line = line.replace('<HEADLINE>', '<field name="tags">')
            line = line.replace('</HEADLINE>', '</field>')
            line = line.replace('<HEAD>', '<field name="categories">')
            line = line.replace('</HEAD>', '</field>')
            line = line.replace('<LEADPARA>', '<field name="description">')
            line = line.replace('</LEADPARA>', '</field>')
            line = line.replace('<TITLE>', '<field name="title">')
            line = line.replace('</TITLE>', '</field>')
            line = line.replace('<TEXT>', '<field name="text">')
            line = line.replace('</TEXT>', '</field>')
            line = line.replace('<LANGUAGE>', '<field name="lang">')
            line = line.replace('</LANGUAGE>', '</field>')
            print(line)

def main():
    if len(sys.argv) < 2:
        printUsageAndExit()
    inputfilename = sys.argv[1]
    print('<add>')
    convertDocs(inputfilename)
    print('</add>')

if __name__ == "__main__":
    # execute only if run as a script
    main()
