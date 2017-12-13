import random
import os
import subprocess


def poolResults(foldername, num_pooling, num_queries):
    # this will take in a single file

    pooled = []
    for _ in range(num_queries):
        pooled.append([])

    files = os.listdir(foldername)
    files = [x for x in files if x.endswith(".out")]

    for filename in files:
        f = open(foldername + "/" + filename, "r")
        content = f.read().strip().splitlines()
        f.close()

        current_query = 1
        for i in range(len(content) - 1):
            words = content[i].split()
            queryid = words[0]
            docid = words[2]
            if queryid == str(current_query):
                for j in range(num_pooling):
                    words = content[i + j].split()
                    docid = words[2]
                    pooled[current_query - 1].append(docid)
                current_query += 1
                if current_query >= num_queries:
                    break

        # the below implentation is more efficeint but
        # only works assuming that earch query actually retrieved all 1000 results
        # for i in range(num_queries):
        #     for line in content[i * num_retrieved : (i * num_retrieved) + num_pooling]:
        #         words = line.split()
        #         pooled[i].append(words[2])

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
    pooled = poolResults(folder, 100, 21)
    createFiles(folder, pooled)
