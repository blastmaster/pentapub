import re
from collections import namedtuple
from datetime import time
from lxml import etree


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


def audacity_marker_to_xml(marker, root):
    ''' transform the Audacity format to xml this involves
        transformation of timestamps and sanitizing the title'''

    start = int(marker.start)
    h = int(start / 3600)
    m = int(start / 60) - h * 60
    s = start % 60
    start_t = time(hour=h, minute=m, second=s)
    title = marker.title.rstrip()
    link = get_link(title)
    attributes = dict(start=start_t.strftime(TIME_FORMAT))
    if link:
        attributes['href'] = link
    for filter_pattern in [LINK_PATTERN, HASHTAG_PATTERN, BULLETPOINT_PATTERN]:
        title = re_filter(title, filter_pattern)
        attributes['title'] = title
    etree.SubElement(root, ELEMENT_NAME, attributes)


def audacity_to_podlove_chapters(filename):
    ''' getting a file which contains the audacity chaptermarks
        retruns the root element of podlove simple xml chaptermarks '''

    with open(filename) as f:
        root = etree.Element('chapters', dict(xmlns='http://podlove.de/simple-chapters'))
        for line in f.readlines():
            marker = AudacityChapterMarks._make(line.split('\t'))
            audacity_marker_to_xml(marker, root)
        return root
