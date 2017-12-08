## Collection of interesting Galago Function:
Source: https://sourceforge.net/p/lemur/wiki/Galago%20Functions/

1. Viewing index of each document:
```bash
$ galago dump-doc-terms --index='<location of postings>' --iddList=1,2,3,4 # Shows the first four documents indexed
$ galago dump-doc-terms --index='./sample_index.postings' --iidList=1,2
```

2. Viewiing the inverted index
````bash
$ galago dump-index <location of posting>
$ galago dump-index ./sample_index/postings
````

3. Statistics for each term:
```bash
# <term> <frequency> <document_count> 
$ galago dump-term-stats ./sample_index/postings
```

4. Miscellaneous functions for inspecting the index
```bash
$ galago dump-index <location of idx>/<?>
$ galago dump-index ./sample_index/lengths # to inspect the length of each document
$ galago dump-index ./sample_index/names # reveal galago's internal state for each DOCNO
$ galago dump-index ./sample_index/names.reverse # above, but reversed
```

This can be combined into one function:
```bash
$ galago dump-name-length --index=./sample_index 
```

