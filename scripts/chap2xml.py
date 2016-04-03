#! /usr/bin/env python3

import sys

from lxml import etree
from pentapub.utils.chaptermarks import audacity_to_podlove_chapters


if len(sys.argv) < 2:
    sys.exit(1)

filename = sys.argv.pop()
root = audacity_to_podlove_chapters(filename)
print(etree.tostring(root, encoding='unicode', pretty_print=True))
