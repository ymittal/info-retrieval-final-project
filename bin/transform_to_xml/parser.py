"""
Run this from the root folder:
$ python bin/transform_to_xml/parser.py <arg1> <arg2>

where
    arg1 is from : ['ar', 'en', 'zh-CN']
    arg2 could be: collection/tedCollection_en
"""

import os
import json
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
  :param subtitle_code: select from the list of ['ar', 'en', 'zh-CN']
  """
  if subtitle_code not in ['ar', 'en', 'zh-CN']:
    raise Exception(
        "Please supply a language code: ['ar', 'en', 'zh-CN']")

  subtitles_dir = os.path.join('subtitles', 'tedEd')
  cwd = os.getcwd()
  folder_names = os.listdir(os.path.join(cwd, subtitles_dir))
  for folder in folder_names:  # EACH VIDEO!
    subtitles = os.listdir(os.path.join(cwd, subtitles_dir, folder))
    for subtitle in subtitles:  # EACH SUBTITLE IN THE VIDEO
      lang = subtitle.split('.', 2)[-2]
      if lang == subtitle_code:
        yield os.path.join(cwd, subtitles_dir, folder, subtitle)


def parse_simple(filepath, language, meta_data, combine=False):
  """
  Following the convention of Trectext, the following tags are used to supply additional metadata for the video:
  1. <DOCNO>      ::  Corresponds to the video id
  2. <Text>       ::  concatenation of the subtitles in the video
  3. <title>      ::  Title of the video
  4. <headline>   ::  The tags the video represents
  5. <leadpara>   ::  the description of the video as in youtube.
  6. <head>       ::  the category the youtube video belongs to
  """
  _et = Element('DOC')

  video_id = str(filepath).split('/')[-2]
  _id = SubElement(_et, 'DOCNO')
  _id.text = video_id.encode('utf-8')
  link = 'https://www.youtube.com/watch?v=' + video_id
  _link = SubElement(_et, 'LINK')
  _link.text = link.encode('utf-8')

  _tags = SubElement(_et, 'HEADLINE')
  _tags.text = meta_data[0]
  _category = SubElement(_et, 'HEAD')
  _category.text = meta_data[1]
  _description = SubElement(_et, 'LEADPARA')
  _description.text = meta_data[2].replace('\\n', '')
  _title = SubElement(_et, 'TITLE')
  _title.text = meta_data[3].replace('\\n', '')

  start = False  # Flag to control when to start including the text.
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
        text += line.decode('utf-8') + ' '

  # Add the text to the file:
  if combine:
    _text.text = ". ".join(
        [meta_data[0], meta_data[1], meta_data[2], meta_data[3], text])
  else:
    _text.text = text

  return _et


def get_meta_data(subtitle_file, language):
  video_id = os.path.basename(os.path.dirname(subtitle_file))
  json_file = os.path.join(os.path.dirname(subtitle_file),
                           video_id + '.info.json')
  with open(json_file) as f:
    datastore = json.load(f, encoding='utf-8')

    tags = datastore['tags']
    cat = datastore["categories"]
    desc = datastore["description"].encode(
        'unicode-escape').encode('utf-8')
    title = datastore["title"].encode('unicode-escape')
    # Standardised for all language to append period after each item in list
    tags = '. '.join(tags)
    cat = '. '.join(cat)
  return [tags, cat, desc, title]


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
  if lang not in ['ar', 'en', 'zh-CN', 'zh-TW']:
    raise Exception(
        "Please supply a language code: ['ar', 'en', 'zh-CN', 'zh-TW']")

  count = 0
  output = sys.argv[2]
  with open(output, 'w') as w:
    all_meta_data = []
    for subtitle_file in gen_files(lang):
      all_meta_data.extend(get_meta_data(subtitle_file, lang))

    meta_data_len = len(all_meta_data)
    if lang != 'en':
      WINDOW = 60
      translated_meta_data = []
      idx = 0
      while idx < meta_data_len:
        if idx + WINDOW < meta_data_len:
          chunk = all_meta_data[idx: idx + WINDOW]
          idx += WINDOW
        else:
          chunk = all_meta_data[idx:]
          idx = meta_data_len
        print('Translating %s subtitles' % (len(chunk) / 4))
        translated_meta_data.extend([x.text for x in translate_all(chunk,
                                                                   fromLanguage='en',
                                                                   toLanguage=lang)])
      assert meta_data_len == len(translated_meta_data)
      all_meta_data = translated_meta_data[:]

    count = 0
    for subtitle_file in gen_files(lang):
      meta_data = all_meta_data[4 * count: 4 * count + 4]
      elem = parse_simple(subtitle_file, lang, meta_data)
      elementTree = ET.ElementTree(elem)
      elementTree.write(w, encoding='utf-8')
      count += 1

print(str(count) + ' files parsed')
