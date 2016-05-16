import re
from collections import namedtuple
from datetime import time
from lxml import etree

from pentapub.utils.time import seconds_to_time

AudacityChapterMarks = namedtuple('AudacityChapterMarks',
                                 ['start', 'end', 'title'])


TIME_FORMAT = '%H:%M:%S'
LINK_PATTERN = re.compile(r'\s?<.*>\s?')
HASHTAG_PATTERN = re.compile(r'(\s?#\w+\s?)+')
BULLETPOINT_PATTERN = re.compile(r'^-*\s')
ELEMENT_NAME = 'chapter'


def get_link(title):
    ''' extract the link from the title if any,
        returns the link as string or None '''

    result = re.search(r'<.*>', title)
    if result:
        return result.string[result.start()+1:result.end()-1]
    return result



def re_filter(title, pattern):
    ''' strip out the pattern from the title '''

    return pattern.sub('', title)


def is_relative_time(timestamp):
    ''' Returns a bool, that indicate if the given timestamp (seconds)
        is less then the length of the production. '''

    # TODO: the length of the production should be a constant or given by some
    # context
    return timestamp < 5400


def convert_timestamp(timestamp, relative_to=0, offset=0):
    ''' Convert the given timestamp (seconds) to a time object with HMS relative to the
        start time of the production, given by the relative_to parameter. 
        Additional an offset can be specified. '''

    if is_relative_time(timestamp):
        tm = seconds_to_time(timestamp)
    else:
        delta = int(timestamp - relative_to - offset)
        tm = seconds_to_time(delta)

    return tm


def audacity_marker_to_xml(marker, root, start_time, offset=0):
    ''' transform the Audacity format to xml this involves
        transformation of timestamps and sanitizing the title'''

    start = int(marker.start)
    start_t = convert_timestamp(start, start_time, offset)
    title = marker.title.rstrip()
    link = get_link(title)
    attributes = dict(start=start_t.strftime(TIME_FORMAT))
    if link:
        attributes.update({'href': link})
    for filter_pattern in [LINK_PATTERN, HASHTAG_PATTERN, BULLETPOINT_PATTERN]:
        title = re_filter(title, filter_pattern)
        attributes.update({'title': title})
    etree.SubElement(root, ELEMENT_NAME, attributes)


def chaptermark_from_file(filename):
    ''' Return an AudacityChapterMarks generator from the given file. '''

    with open(filename) as f:
        for line in f.readlines():
            yield AudacityChapterMarks._make(line.split('\t'))


def audacity_to_podlove_chapters(filename, start_time=0, offset=0):
    ''' Retrun the xml root element of podlove simple chapters formatted
        chaptermarks.
        filename: str filename of chaptermarks file (Audacity Chaptermarks only atm.)

        start_time: unix timestamp of the podcast recording start, to adjust other timestamps relative to this time.
                    If start_time is 0 (default) then the first timestamp in the
                    chaptermarks file will be used as base.

        offset: int an additional timestamp offset in seconds.

        FIXME: start_time and offset are somewhat redundant
    '''

    root = etree.Element('chapters', dict(xmlns='http://podlove.de/simple-chapters'))
    chaptermark_gen = chaptermark_from_file(filename)

    if start_time == 0:
        first_mark = next(chaptermark_gen)
        start_time = int(first_mark.start)

    for mark in chaptermark_gen:
        audacity_marker_to_xml(mark, root, start_time, offset)

    return root
