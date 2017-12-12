"""
Run this from the root folder:
$ python bin/transform_to_xml/parser.py
"""

import os, json, re
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET


def gen_files(subtitle_code=None):
    """
    :param subtitle_code: select from the list of ['ar', 'en', 'zh-CN', 'zh-TW']
    """
    assert subtitle_code is not None, "Please supply a language code: ['ar', 'en', 'zh-CN', 'zh-TW']"
    cwd = os.getcwd()
    folder_names = os.listdir('./tedDirector')
    for folder in folder_names:  # EACH VIDEO!
        subtitles = os.listdir(cwd + '/tedDirector/' + folder)
        for subtitle in subtitles:  # EACH SUBTITLE IN THE VIDEO
            lang = subtitle.split('.', 2)[-2]
            if lang == subtitle_code:
                filepath = cwd + '/tedDirector/' + folder + '/' + subtitle
                yield filepath


def parse_simple(filepath, language):
    """
    Following the convention of Trectext, the following tags are used to supply additional metadata for the video:
    1. <DOCNO>      ::  Corresponds to the video id
    2. <Text>       ::  concatenation of the subtitles in the video
    3. <title>      ::  Title of the video
    4. <headline>   ::  The tags the video represents
    5. <leadpara>   ::  the description of the video as in youtube.
    6. <head>       ::  the category the youtube video belongs to
    """
    start = False  # Flag to control when to start including the text.
    _et = Element('DOC')

    video_id = str(filepath).split('/')[-2]
    _id = SubElement(_et, 'DOCNO')
    _id.text = video_id.encode('utf-8')
    link = 'https://www.youtube.com/watch?v=' + video_id
    _link = SubElement(_et, 'LINK') # this will not be read by trec parser.
    _link.text = link.encode('utf-8')

    # add meta information
    jsonFile = "/".join(str(filepath).split('/')[:-1]) + '/' + video_id + '.info.json'
    with open(jsonFile) as f:
        datastore = json.load(f, encoding='utf-8')
        tags = " ".join(datastore['tags'])
        _tags = SubElement(_et, 'HEADLINE')
        _tags.text = tags
        # print tags

        cat = " ".join(datastore['categories'])
        _category = SubElement(_et, 'HEAD')
        _category.text = cat
        # print cat

        desc = datastore["description"].encode('unicode-escape').encode('utf-8')
        _description = SubElement(_et, 'LEADPARA')
        _description.text = desc.replace('\\n','')
        # print desc

        title = datastore["title"].encode('unicode-escape')
        _title = SubElement(_et, 'TITLE')
        _title.text = title
        # print title

    _text = SubElement(_et, 'TEXT')
    text = ""
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # print type(line) #DEBUG
            if line.startswith('Language:'):
                _, lang = line.split(': ', 1)
                _lang = SubElement(_et, 'LANGUAGE')
                _lang.text = lang.encode('utf-8')
                print(lang)

            elif '-->' in line:
                # Ignore the timestamps
                start = True
                continue

            elif line and start:
                # if language == 'en':
                #     text += line.decode() + ' '
                #     # print line
                # else:
                text += line.decode('utf-8') + ' '

    # Add the text to the file:
    _text.text = text

    return _et


def parse_timestamp(filepath, language):
    """
    Parse the file given in the argument, filePath according to the VTT format.
    dump the filepath in writeFile.
    <SUBTITLE>
        <VIDEOID>  </VIDEOID>
        <LANGUAGE>  </LANGUAGE>
        <CAPTION>
            <TEXT>
            <STARTTIME> </STATTIME>
            <ENDTIME> </ENDTIME>
        </CAPTION>
    </SUBTITLE>
    :param filepath: the file to write
    :return: ET.toSting(elemenTree)
    """
    video_id = str(filepath).split('/')[-2]
    timeStep = None
    _attributes = {"start": None, "end": None}
    attributes = _attributes
    with open(filepath, 'r') as f:
        _et = Element('SUBTITLE')
        _id = SubElement(_et, 'VIDEOID')
        _id.text = video_id.encode('utf-8')

        for line in f:
            line = line.strip()
            # print type(line) #DEBUG
            if line.startswith('Language:'):
                _, lang = line.split(': ', 1)
                _lang = SubElement(_et, 'LANGUAGE')
                _lang.text = lang.encode('utf-8')
                print(lang)

            elif '-->' in line:
                start, end = line.split('-->')
                # _startTime = SubElement(_caption, 'STARTTIME')
                # _endTime = SubElement(_caption, 'ENDTIME')
                attributes['start'] = start.strip().encode('utf-8')
                attributes['end'] = end.strip().encode('utf-8')
                # _startTime.text = start.strip()
                # _endTime.text = end.strip()
                _caption = SubElement(_et, 'CAPTION', attrib=attributes)
                timeStep = _caption

            elif line:
                if timeStep is not None:
                    # print(line)
                    # if lang == 'en':
                    #     timeStep.text = line
                    # elif lang == 'ar':
                    # timeStep.text = line.decode('utf-8') # this works, means that the line is already in unicode!
                    timeStep.text = line.decode('utf-8')
                else:
                    timeStep = None
                    continue
    # try:
    #     output = tostring(_et, encoding='unicode')
    # except TypeError:
    # output = tostring(_et)  # Return in US_ASCII!
    # output = tostring(_et, encoding='utf-8')  # Return in unicode!
    # print(output)
    return _et


if __name__ == "__main__":
    lang = 'en'
    count = 0

    with open('collection/tedDirector_en', 'w') as w:
        for sub in gen_files(lang):
            count += 1
            elem = parse_simple(sub, lang)
            elementTree = ET.ElementTree(elem)
            elementTree.write(w, encoding='utf-8')
            # w.write('\n')
    print(str(count) + ' files parsed')
