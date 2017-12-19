
import sys

def printUsageAndExit():
    args = " input_file"
    print("Usage: " + sys.argv[0] + args, file=sys.stderr)
    sys.exit(1)

def normalise(word):
    # special cases
    if word in ('IoT', 'AI'):
        return word
    # casefold the rest
    return word.lower()

def makeQuery(num, line):
    terms = ['#bm25({})'.format(normalise(word)) for word in line.split()]
    query = '    {\n'
    query += '      "number" : "{}",\n'.format(num+1)
    query += '      "text"   : "#combine({})"\n'.format(' '.join(terms))
    query += '    }'
    return query

def makeQueries(filename):
    with open (filename) as f:
        print(',\n'.join([makeQuery(num, line) for num, line in enumerate(f)]))

def main():
    if len(sys.argv) < 2:
        printUsageAndExit()
    inputfilename = sys.argv[1]
    print("""{
  "casefold": true,
  "fields": [
    "text",
    "headline",
    "title",
    "head",
    "leadpara"
  ],
  "index": "../idx/tedDirector_en.idx",
  "verbose": true,
  "requested": 1000,
  "queries"  : [""")
    makeQueries(inputfilename)
    print(' ]\n}')

if __name__ == "__main__":
    # execute only if run as a script
    main()
