# from __future__ import unicode_literals
import os
from xml.etree.ElementTree import Element, SubElement, dump, tostring


def gen_files():
  cwd = os.getcwd()
  folder_names = os.listdir('./tedDirector')
  for folder in folder_names:
    subtitles = os.listdir(cwd + '/tedDirector/' + folder)
    for subtitle in subtitles:
      filepath = cwd + '/tedDirector/' + folder + '/' + subtitle
      yield filepath


def parse(filepath):
  video_id = str(filepath).split('/')[-2]
  timeStep = None
  with open(filepath, 'r') as f:
    _et = Element('SUBTITLE')
    _id = SubElement(_et, 'VIDEO_ID')
    _id.text = video_id

    for line in f:
      line = line.strip()
      # print type(line)
      if line.startswith('Language:'):
        _, lang = line.split(': ', 1)
        _lang = SubElement(_et, 'LANGUAGE')
        _lang.text = lang

      elif '-->' in line:
        start, end = line.split('-->')
        _timeStep = SubElement(_et, 'TIMESTEP')
        _startTime = SubElement(_timeStep, 'STARTTIME')
        _endTime = SubElement(_timeStep, 'ENDTIME')
        _startTime.text = str(start)
        _endTime.text = str(end)
        timeStep = _timeStep

      elif line:
        if timeStep is not None:
          print(line)
          _caption = SubElement(timeStep, 'CAPTION')
          _caption.text = line.decode('utf-8')
        else:
          timeStep = None
          continue
  # print tostring(_et)

# if __name__ == "__main__":
#   generator = gen_files()
#   while sub in generator:
