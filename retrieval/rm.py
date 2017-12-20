
import re
import sys

def printUsageAndExit():
    args = " input_file"
    print("Usage: " + sys.argv[0] + args, file=sys.stderr)
    sys.exit(1)

def makeQuery(num, line):
    # remove punctuation
    line = re.sub('\W', ' ', line)
    terms = [word for word in line.split()]
    query = '    {\n'
    query += '      "number": "{}",\n'.format(num+1)
    query += '      "scorer" : "bm25",\n'
    query += '      "text": "{}"\n'.format(' '.join(terms))
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
  "verbose": true,
  "fields": [
    "text",
    "headline",
    "title",
    "head",
    "leadpara"
  ],
  "index": ["../idx/tedDirector_en.idx", "../idx/tedX_en-ALL.idx", "../idx/tedEd_en-ALL.idx"],
  "requested": 1000,
  "fbDocs": 10,
  "fbTerm": 10,
  "fbOrigWeight": 0.75,
  "operatorWrap": "rm",
  "queries": [""")
    makeQueries(inputfilename)
    print('  ]\n}')

if __name__ == "__main__":
    # execute only if run as a script
    main()
