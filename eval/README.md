## All evaluation stuff goes in here!

The judgement results will be added here as qrels.txt
The order of entries in the file is not important.

They need to be filtered by language as follows:

grep -F -f idx.ar qrels.txt > qrels.ar
grep -F -f idx.en qrels.txt > qrels.en
grep -F -f idx.zh-CN qrels.txt > qrels.zh-CN

This ensures that only files which are available in the relevant language 
are considered when judging the output of each system.

For example, it would be wrong to penalise a system that used only Arabic 
data for missing some relevant documents that were only available in 
English.

---
## Log
Jan 4 :: Added provisional qrels based on the queries that are judged.
