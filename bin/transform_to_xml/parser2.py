"""
Run this from the root folder:
$ python bin/transform_to_xml/parser.py
"""

import os
import json
import re
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
from googletrans import Translator


def translate_all(data, fromLanguage, toLanguage):
    translator = Translator(service_urls=['translate.google.com',
                                          'translate.google.com.hk',
                                          'translate.google.com.tw'])
    return translator.translate(data, dest=toLanguage, src=fromLanguage)


def gen_files(subtitle_code=None):
    """
    TODO: there's a lot of hard cord part here ! Might be worth fixing
    :param subtitle_code: select from the list of ['ar', 'en', 'zh-CN', 'zh-TW']
    """
    if subtitle_code not in ['ar', 'en', 'zh-CN', 'zh-TW']:
        raise Exception(
            "Please supply a language code: ['ar', 'en', 'zh-CN', 'zh-TW']")

    subtitles_dir = os.path.join('subtitles', 'tedEd')
    cwd = os.getcwd()
    folder_names = os.listdir(os.path.join(cwd, subtitles_dir))
    for folder in folder_names:  # EACH VIDEO!
        subtitles = os.listdir(os.path.join(cwd, subtitles_dir, folder))
        for subtitle in subtitles:  # EACH SUBTITLE IN THE VIDEO
            lang = subtitle.split('.', 2)[-2]
            if lang == subtitle_code:
                yield os.path.join(cwd, subtitles_dir, folder, subtitle)


def parse_simple(filepath, language, meta_data):
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

    video_id = os.path.basename(os.path.dirname(subtitle_file))
    _id = SubElement(_et, 'DOCNO')
    _id.text = video_id.encode('utf-8')
    link = 'https://www.youtube.com/watch?v=' + video_id
    _link = SubElement(_et, 'LINK')  # this will not be read by trec parser.
    _link.text = link.encode('utf-8')

    # add meta information
    jsonFile = "/".join(str(filepath).split('/')
                        [:-1]) + '/' + video_id + '.info.json'
    with open(jsonFile) as f:
        datastore = json.load(f, encoding='utf-8')
        # tags = " ".join(datastore['tags'])
        # cat = " ".join(datastore['categories'])
        tags = datastore['tags']
        cat = datastore['categories']
        desc = datastore["description"].encode(
            'unicode-escape').encode('utf-8')
        title = datastore["title"].encode('unicode-escape')
        if language != 'en':
            # append fullstop so that each word/phrase is independent from each
            # other in the MT system
            tags = '. '.join(tags)
            cat = '. '.join(cat)
            tags, cat, desc, title = translate(
                tags, cat, desc, title, fromLanguage='en', toLanguage=language)

    _tags = SubElement(_et, 'HEADLINE')
    _tags.text = tags
    _category = SubElement(_et, 'HEAD')
    _category.text = cat
    _description = SubElement(_et, 'LEADPARA')
    _description.text = desc.replace('\\n', '')
    _title = SubElement(_et, 'TITLE')
    _title.text = title

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


def get_meta_data(subtitle_file, language):
    video_id = os.path.basename(os.path.dirname(subtitle_file))
    json_file = os.path.join(os.path.dirname(subtitle_file),
                             video_id + '.info.json')
    with open(json_file) as f:
        datastore = json.load(f, encoding='utf-8')
        print(datastore)

        tags = datastore['tags']
        cat = datastore["categories"]
        desc = datastore["description"].encode(
            'unicode-escape').encode('utf-8')
        title = datastore["title"].encode('unicode-escape')

        if language != 'en':
            # append fullstop so that each word/phrase is independent from each
            # other in the MT system
            tags = '. '.join(tags)
            cat = '. '.join(cat)

    return [tags, cat, desc, title]

if __name__ == "__main__":
    import sys
    lang = sys.argv[1]
    if lang not in ['ar', 'en', 'zh-CN', 'zh-TW']:
        raise Exception(
            "Please supply a language code: ['ar', 'en', 'zh-CN', 'zh-TW']")

    count = 0
    output = sys.argv[2]
    with open(output, 'w') as w:
        all_meta_data = []
        for subtitle_file in gen_files(lang):
            all_meta_data.append(get_meta_data(subtitle_file, lang))

        if lang != 'en':
            all_meta_data = translate_all(all_meta_data,
                                                  fromLanguage='en',
                                                  toLanguage=lang)

        count = 0
        for subtitle_file in gen_files(lang):
            meta_data = all_meta_data[count]
            print(meta_data)
            # elem = parse_simple(subtitle_file, lang, meta_data)
            # elementTree = ET.ElementTree(elem)
            # elementTree.write(w, encoding='utf-8')
            count += 1

    print(str(count) + ' files parsed')
