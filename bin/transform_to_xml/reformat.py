import os

def reformat_captions():
    f = open("subtitles.xml", "w+")

    path = "../../subtitles/"
    videos = os.listdir( path )
    for docnum in range(len(videos)):

        # print(video_dir)
        video_dir = videos[docnum]
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
                s = "<DOC>\n<DOCNO>\n{}\n</DOCNO>\n".format(docnum)
                s += "<VIDEOID>\n{}\n</VIDEOID>\n".format(video_dir)
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

                s += "\n</TEXT>\n</DOC>\n"

                f.write(s)
                break

    f.close()

reformat_captions()
