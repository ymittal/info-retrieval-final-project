import os
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
    Parse all the files in the corresponding filePath, but ignore
    :param filepath:
    :param language:
    :return:
    """
    start = False # Flag to control when to start including the text.
    video_id = str(filepath).split('/')[-2]
    link = 'https://www.youtube.com/watch?v=' + video_id

    with open(filepath, 'r') as f:
        _et = Element('DOC')
        _id = SubElement(_et, 'DOCNO')
        _id.text = video_id.encode('utf-8')

        _link = SubElement(_et, 'LINK')
        _link.text = link.encode('utf-8')

        _text = SubElement(_et, 'TEXT')
        text = ""

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

            elif line and start :
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
    lang = 'zh-CN'
    count = 0

    with open('tedDirector_zh-CN', 'w') as w:
        for sub in gen_files(lang):
            count += 1
            elem = parse_simple(sub, lang)
            elementTree = ET.ElementTree(elem)
            elementTree.write(w, encoding='utf-8')
            # w.write('\n')
    print(str(count) + ' files parsed')
