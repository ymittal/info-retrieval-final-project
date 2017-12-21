
import os
import pooling

if __name__ == '__main__':
    """
    Run this in the retrieval folder!
    """
    # folder is directory containing all results
    # each results file all the queries for one system
    folder = os.getcwd()
    print 'Pooling top 100 results for each query: ', str(folder)
    pooled = pooling.poolResults(folder, 100, 25) # 25 queries
    pooling.createFiles(folder, pooled)
