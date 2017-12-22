This folder contains:
1. Queries for evaluating our systems
2. Configuration files for searching

Using `Galago`, we analysed the following:
1. Retrieval performance using different query operators:
    - BM25
    - Relevance model (RM)
    - Sequential Dependece model (SDM)
2. Difference in performance with addition of query description

Hence, a total of six different retrieval configurations were created.

After the results were generated, the top 100 results for each system were pooled and shuffled. The enquire then conduct relevance judgement on each of this videos, ascertaining their relevancy to the query.
