"""
Trialing with pylucene - can it index files in different languages?
"""

import os, re, lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import BytesRef, BytesRefIterator

if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    store = SimpleFSDirectory(Paths.get('../../idx/Index_en.index'))
    analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1000)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    # Define FieldTypes - elements tht we want each document to contain
    DOCNO = FieldType()
    DOCNO.setStored(True)
    DOCNO.setTokenized(False)
    DOCNO.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    LINK = FieldType()
    LINK.setStored(True)
    LINK.setTokenized(False)
    LINK.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    TAGS = FieldType()
    TAGS.setStored(True)
    TAGS.setTokenized(True)
    TAGS.setStoreTermVectors(True)
    TAGS.setStoreTermVectorPositions(True)
    TAGS.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    with open('../../collection/tedDirector_en') as f:
        doc = None
        for line in f:
            line = line.strip()

            if '<DOC>' in line:
                doc = Document() # set a store for this document
                continue

            if '<DOCNO>' in line:
                l = f.next()
                docno = l[:-8]
                doc.add(Field("docno", docno, DOCNO))
                continue

            if '<LINK>' in line:
                l = f.next()
                link = l[:-7]
                doc.add(Field("link", link, LINK))
                continue

            if '<TAGS>' in line:
                l = f.next()
                tag = l[:-7]
                doc.add(Field("tags", tag, TAGS))
                continue


            if '</DOC>' in line:
                writer.addDocument(doc)
                doc = None
                continue


    writer.commit()
    writer.close()
    print 'IndexFiles: done'


    # Print the term vector:
    if DirectoryReader.indexExists(store):
        print 'exists'
    reader = DirectoryReader.open(store)
    for i in range(reader.getDocCount('tags')):
        tv = reader.getTermVector(i, 'tags')
        termsEnum = tv.iterator()

        for term in BytesRefIterator.cast_(termsEnum):
            dpEnum = termsEnum.postings(None)
            dpEnum.nextDoc()  # prime the enum which works only for the current doc
            freq = dpEnum.freq()

            print 'term:', term.utf8ToString()
            print '  freq:', freq

            for i in xrange(freq):
                print "  pos:", dpEnum.nextPosition()
                print "  off: %i-%i" % (dpEnum.startOffset(), dpEnum.endOffset())
        print
