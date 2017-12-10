## How to lucene

0. Fetch this branch if you havent already:
```bash
$ git fetch orgin
$ git checkout -b origin/lucene
```

1. Download the jar files for [lucene 7.1.0](http://www.apache.org/dyn/closer.lua/lucene/java/7.1.0); extract it and move it to outside the repository (depending on how and where you like it actually)

2. Open your favourite java ide (I used intellij) - and add the following `jar` files into the library:
  1. lucene-core.jar
  2. lucene-demo.jar
  3. lucene-analyzers-common.jar

3. write some java code for lucene! The `indexFiles2.java` from [here](https://github.com/jiepujiang/cs646_tutorials) is a very good starting point, as it is closer to what we have right now.

---
***Talk about reinventing the wheel the hard way~***
