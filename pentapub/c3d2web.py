import os
from string import Template

from lxml import etree

from pentapub.utils.chaptermarks import audacity_to_podlove_chapters

'''
Filling out the resource tag for c3d2-web.

Example:
  <resource title="pentaradio24 vom 23. Juni 2015"
        size="92839165"
        type="application/ogg"
        url="http://ftp.c3d2.de/pentaradio/pentaradio-2015-06-23.ogg">
    <alternative size="84459626"
                 type="audio/mpeg"
                 url="http://ftp.c3d2.de/pentaradio/pentaradio-2015-06-23.mp3"/>
    <alternative size="39017524"
                 type="audio/opus"
                 url="http://ftp.c3d2.de/pentaradio/pentaradio-2015-06-23.opus"/>
    <chapters xmlns="http://podlove.de/simple-chapters">
      <chapter start="0:00:00" title="News"/>
      <chapter start="0:18:31" title="Musik: Write in C"/>
      <chapter start="0:22:04" title="Thema"/>
      <chapter start="1:11:00" title="Musik: The Java Life"/>
      <chapter start="1:14:13" title="Thema"/>
    </chapters>
  </resource>

Required Information:
    title: (text)
    size: (in bytes)
    type: (mime type)
    url: (http)

How to get these information:

    size: os.path.getsize() -> get size in bytes
        -rw-r--r--    1 1021     ftpupload 67576682 Mar 29 16:12 pentaradio-2016-03-22.ogg
        -rw-r--r--    1 1021     1017     40876075 Mar 29 16:18 pentaradio-2016-03-22.opus
        -rw-r--r--    1 1021     1017     75086002 Mar 29 16:20 pentaradio-2016-03-22.mp3

    type:
        via subprocess and file:
            file -b --mime-type <file>
        or via mimetypes standard library module:
'''


def write_resource(main_attrs, alts):
    ''' writes the xml resource tag for c3d2-web news entry '''

    root = etree.Element('resource', main_attrs)
    for alt in alts:
        etree.SubElement(root, 'alternative', alt)
    return root


def append_chaptermarks(root, filename):
    ''' appends chaptermarks to the given root element '''

    chapters = audacity_to_podlove_chapters(filename)
    root.append(chapters)


def build_c3d2_news_entry(production, filename):
    ''' takes a production object and a filename to the chaptermarks.
        builds the c3d2-web news resource tag and returns the root element of the tag. '''

    main_resource = production['ogg']._asdict()
    main_resource['title'] = production.title
    alternatives = [production['mp3']._asdict(), production['opus']._asdict()]

    resource = write_resource(main_resource, alternatives)
    if filename:
        append_chaptermarks(resource, filename)

    return resource



class c3d2News:

    BASENAME_TEMPLATE = Template('pentaradio24-$date')

    DATE_FORMAT = '%Y%m%d'

    NEWS_DIR = 'content/news/'

    def __init__(self, git_root):

        if not os.path.exists(git_root):
            raise ValueError('git_root: {0} directory does not exists'.format(git_root))

        self.git_root = git_root


    def news_from_date(self, date):
        ''' Builds and returns the path to the news file in c3d2-web. '''

        date_str = date.strftime(self.DATE_FORMAT)
        path = os.path.join(self.git_root, self.NEWS_DIR)
        filename = self.BASENAME_TEMPLATE.substitute(date=date_str) + '.xml'
        return os.path.join(path, filename)

    def news_from_production(self, production):
        ''' Builds and returns the path to the news file in c3d2-web. '''

        return self.news_from_date(production.date)

    def write_news(self, production, chapterfile=None, outfile=None):
        ''' writes the resource tag to c3d2-web '''

        newsfile = self.news_from_production(production)
        if not outfile:
            outfile = newsfile
        tree = etree.parse(newsfile)
        root = tree.getroot()
        resource_tag = build_c3d2_news_entry(production, chapterfile)
        root.append(resource_tag)

        # FIXME: if outfile is an open file like sys.stdout the call to open
        # caused a TypeError. But we want to print to stdout so we need a
        # exception. Is there a better way to handle this?

        # TODO: bring some output where you wrinting to!

        try:
            f = open(outfile, 'w', encoding='UTF-8')
        except TypeError:
            f = outfile
        # TODO: pretty printing is not that much pretty! all in one line :(
        f.write(etree.tostring(root, encoding='unicode', pretty_print=True))
