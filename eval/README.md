## All evaluation stuff goes in here!

The judgement results will be added here as qrels.txt
The order of entries in the file is not important.

They need to be filtered by language as follows:

```bash
$ grep -F -f idx.ar qrels.txt > qrels.ar
$ grep -F -f idx.en qrels.txt > qrels.en
$ grep -F -f idx.zh-CN qrels.txt > qrels.zh-CN
```

This ensures that only files which are available in the relevant language
are considered when judging the output of each system.

For example, it would be wrong to penalise a system that used only Arabic
data for missing some relevant documents that were only available in
English.

---
## Log
Jan 4 :: Added provisional qrels based on the queries that are judged.

Jan 8 :: Generated qrels with queries #1,5,7,8,9,10,11,12,13,14,15,16,22,23,25; and generated individual qrels for each language.

Jan 11 :: Generated qrels with queries #1,5,7,8,9,10,11,12,13,14,15,16,17,19,22,23,25; and re-generated individual qrels for each language.
in (analysis)[../analysis] folder, `treceval` will be used to analysis the system (galago and solr) and compare the different retrieval functions used.
