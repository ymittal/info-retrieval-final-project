import os

def reformat_captions():
    f = open("subtitles.xml", "w+")

    path = "./subtitles/"
    videos = os.listdir( path )
    doc_num = 1
    for video_dir in videos:
        # print(video_dir)
        if video_dir.startswith("."):
            continue

        languages = os.listdir( path + video_dir )
        for language in languages:
            if language.split('.')[1] == 'en':
                # print(path + video_dir + "/" + language)
                filename = path + video_dir + "/" + language
                f2 = open(filename, "r")
                captions = f2.read().strip().splitlines()
                f2.close()
                s = "<DOC>\n<DOCNO>{}</DOCNO>\n".format(doc_num)
                s += "<TEXT>\n"

                i = 0
                while i < len(captions):
                    if captions[i] == '':  # this is the new line before a timestamp
                        i += 2
                        while (i < len(captions) and captions[i] != ""):
                            s += captions[i] + " "
                            i += 1
                    else:
                        i += 1

                s += "</TEXT>\n</DOC>\n"

                f.write(s)
                break

        doc_num += 1

    f.close()

reformat_captions()
