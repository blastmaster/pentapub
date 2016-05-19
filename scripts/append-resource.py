#! /usr/bin/env python3

import sys
import argparse
from datetime import date

from pentapub.c3d2web import c3d2News
from pentapub.production import Production
from pentapub.utils.time import get_rec_date

''' Append resource tag to news and writes xml to stdout '''

parser = argparse.ArgumentParser(description='create c3d2.de news and writes to stdout')
parser.add_argument('--git-root', required=True, type=str, help='the root of the c3d2-web.git')
parser.add_argument('--working-dir', required=True, type=str, help='the working directory, in this directory resists the audio files of the pentaradio production')
parser.add_argument('--chapterfile', type=str, help='file contains the chaptermarks')
parser.add_argument('--month', type=int, help='month of the production')
parser.add_argument('--year', type=int, help='year of the production')
parser.add_argument('--day', type=int, help='day of the production')

args = parser.parse_args()

#TODO: Urrrghs!
try:
    d = date(year=args.year, month=args.month, day=args.day)
except TypeError:
    d = get_rec_date(year=args.year, month=args.month)

prod = Production(working_dir=args.working_dir, prod_date=d)
news = c3d2News(git_root=args.git_root)
#FIXME: throws an non obivous exception if no audio files where found
news.write_news(prod, args.chapterfile, outfile=sys.stdout)
