import random
import os
import subprocess

random.seed(20171221)

def poolResults(foldername, num_pooling, num_queries):
    # this will take in a single file

    pooled = []
    for _ in range(num_queries):
        pooled.append([])

    files = os.listdir(foldername)
    files = [x for x in files if x.endswith(".out")]

    for filename in files:
        with open(foldername + "/" + filename, "r") as f:
            current_query = 1
            current_result = 0
            for line in f:
                words = line.split()
                queryid = words[0]
                docid = words[2]
                if queryid == str(current_query):
                    if current_result < num_pooling:
                        pooled[current_query - 1].append(docid)
                        current_result += 1
                    else:
                        current_query += 1
                        current_result = 0
                        if current_query >= num_queries:
                            break

    return shuffle(pooled)


def shuffle(lists):
    shuffled = []
    for l in lists:
        l = list(set(l))
        random.shuffle(l)
        shuffled.append(l)
    return shuffled


def createFiles(foldername, pooled_results):
    for i in range(len(pooled_results)):
        f = open("{}/Q{}.results".format(foldername, i + 1), "w+")
        f.write("\n".join(pooled_results[i]))
        f.close()


if __name__ == '__main__':
    """
    Run this in the retrieval folder!
    """
    files = os.listdir(os.getcwd())
    for file in files:
        if str(file).endswith('.json'):
            output_name = file[:-5] + '.out'
            logger_name = file[:-5] + '.log'
            subprocess.call(['/home/goweiting/Documents/TTDS/galago-3.12-bin/bin/galago', 'batch-search', file],
                            stdout=open(output_name, 'w'), stderr=open(logger_name, 'w'))
            print file, '\t=>\t', output_name

    # folder is directory containing all results
    # each results file all the queries for one system
    folder = os.getcwd()
    print 'Pooling top 100 results for each query: ', str(folder)
    pooled = poolResults(folder, 100, 25) # 25 queries
    createFiles(folder, pooled)
