"""
Run this from the root folder:
$ python bin/transform_to_xml/parser.py <arg1> <arg2>

where
    arg1 is from : ['ar', 'en', 'zh-CN', 'zh-TW']
    arg2 could be: collection/tedCollection_en
"""

import os
import json
import re
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
from googletrans import Translator


def translate(tags, cat, desc, title, fromLanguage, toLanguage):
  translator = Translator(service_urls=[
                          'translate.google.com', 'translate.google.com.hk', 'translate.google.com.tw'])
  # Bulk process
  _tags, _cat, _desc, _title = translator.translate(
      [tags, cat, desc, title], dest=toLanguage, src=fromLanguage)
  return _tags.text, _cat.text, _desc.text, _title.text


def gen_files(subtitle_code=None):
  """
  TODO: there's a lot of hard cord part here ! Might be worth fixing
  :param subtitle_code: select from the list of ['ar', 'en', 'zh-CN', 'zh-TW']
  """
  assert subtitle_code is not None, "Please supply a language code: ['ar', 'en', 'en-US','en-GB',zh-CN', 'zh-TW']"
  cwd = os.getcwd()
  # folders = ['./subtitles/tedDirector', './subtitles/tedEd', './subtitles/tedX']
  # for f in folders:
  # folder_names = os.listdir(f)
  folder_names = os.listdir('./subtitles/tedEd')
  for folder in folder_names:  # EACH VIDEO!
    subtitles = os.listdir(cwd + '/subtitles/tedEd/' + folder)
    for subtitle in subtitles:  # EACH SUBTITLE IN THE VIDEO
      lang = subtitle.split('.', 2)[-2]
      if lang == subtitle_code:
        filepath = cwd + '/subtitles/tedEd/' + folder + '/' + subtitle
        yield filepath


def parse_simple(filepath, language, combine=False):
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
    desc = datastore["description"].encode('unicode-escape').encode('utf-8')
    title = datastore["title"].encode('unicode-escape')
    tags = '. '.join(tags)
    cat = '. '.join(cat)
    if language[:2] != 'en':
      # append fullstop so that each word/phrase is independent from each other
      # in the MT system
      tags, cat, desc, title = translate(
          tags, cat, desc, title, fromLanguage='en', toLanguage=language)

  _tags = SubElement(_et, 'HEADLINE')
  _tags.text = tags
  _category = SubElement(_et, 'HEAD')
  _category.text = cat
  _description = SubElement(_et, 'LEADPARA')
  desc = desc.replace('\\n', '')
  _description.text = desc
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
        # print(lang)

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
  if combine:
    _text.text = ". ".join([tags, cat, desc, title, text])
  else:
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
          # timeStep.text = line.decode('utf-8') # this works, means that the
          # line is already in unicode!
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
  import sys
  lang = sys.argv[1]
  count = 0

  output = sys.argv[2]
  with open(output, 'w') as w:
    for sub in gen_files(lang):
      count += 1
      elem = parse_simple(sub, lang, combine=False)
      elementTree = ET.ElementTree(elem)
      elementTree.write(w, encoding='utf-8')
  print(str(count) + ' files parsed')
