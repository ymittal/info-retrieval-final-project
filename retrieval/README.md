This folder contains:
1. Queries for evaluating our systems
2. Configuration files for searching in Galago
3. Raw and processed results from Solr

Experiment 1 (Galago)

Using `Galago`, we analysed the following:
1. Retrieval performance using different query operators:
    - BM25
    - Relevance model (RM)
    - Sequential Dependece model (SDM)
2. Difference in performance with addition of query description

Hence, a total of six different retrieval configurations were created.

Experiment 2 (Solr)

Using `Solr`, we ran our queries in English, Arabic, and Chinese, using 
the same search parameters for all the searches.
We compared using topic titles alone, and title + description.

Again, a total of six different configurations were used.


After all the results were generated, the top 100 results for each system 
were pooled and shuffled. The team then made relevance judgements to 
identify whether each result was relevant to the query.
