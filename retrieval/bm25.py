
with open ("titels.txt") as f:
    for line in f:
        print ("#combine(",end='')
        for word in line.split():
            print("#bm25(" + word + ") ",end='')
        print (")")

