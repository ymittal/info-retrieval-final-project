
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
  query += '      "number": "{}",\n'.format(num + 1)
  query += '      "scorer" : "bm25",\n'
  query += '      "text": "{}"\n'.format(' '.join(terms))
  query += '    }'
  return query


def makeQueries(filename):
  with open(filename) as f:
    print(',\n'.join([makeQuery(num, line) for num, line in enumerate(f)]))


def main():
  if len(sys.argv) < 2:
    printUsageAndExit()
  inputfilename = sys.argv[1]
  print("""{
  "casefold": true,
  "verbose": true,
  "index": ["../../idx/galago/ted.en.idx"],
  "requested": 1000,
  "operatorWrap": "sdm",
  "queries": [""")
  makeQueries(inputfilename)
  print('  ]\n}')


if __name__ == "__main__":
  # execute only if run as a script
  main()
