import os
from string import Template
import mimetypes
from collections import namedtuple

from pentapub.utils.time import get_rec_date


def audio_production_from_name(filename):
    ''' gathers the metadata of the given filename.
        returns a AudioProduction type '''

    prod_size = os.path.getsize(filename)
    mime_type = mimetypes.guess_type(filename)[0]
    # TODO:
    prod_url = 'http://ftp.c3d2.de/pentaradio/' + os.path.basename(filename)
    return AudioProduction(size=str(prod_size),
                           type=mime_type,
                           url=prod_url)


AudioProduction = namedtuple('AudioProduction', ['size', 'type', 'url'])


class Production:
    '''
        The Production class represents a pentaradio production.
        A Production consists of the following attributes:

        date -  a datetime.date object of the date of the recording
                of that production.

        _productions - a dict containing AudioProduction elements as values
        and audio format extension as key.
    '''

    BASENAME_TEMPLATE = Template('pentaradio-$date')

    TITLE_TEMPLATE = Template('pentaradio24 vom $date')

    DATE_FORMAT = '%Y-%m-%d'


    def __init__(self, working_dir=os.getcwd(), prod_date=get_rec_date(), **kwargs):

        self.date = prod_date
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._productions = self.retrieve_productions(working_dir)


    def __getitem__(self, key):
        ''' make Production subscriptable by AudioProduction extension '''

        return self._productions[key]

    @property
    def title(self):
        ''' Returns the title of the pentaradio production. '''

        time_fmt = '%d. %B %Y'
        return self.TITLE_TEMPLATE.substitute(date=self.production_date(time_fmt))

    @property
    def basename(self):
        ''' Returns the basename of a pentaradio production as string. '''

        return self.BASENAME_TEMPLATE.substitute(date=self.production_date())

    def retrieve_productions(self, path):
        ''' search in the given path for all files which match the pentaradio
            name convention using the basename for searching.

            return a dict where the extension is the key and the value are
            Audioproduction tuples which contain the metadata. '''

        productions = {}
        for dentry in os.listdir(path):
            if dentry.startswith(self.basename):
                filename = os.path.join(path, dentry)
                sidx = dentry.rfind('.')
                key = dentry[sidx+1:]
                productions[key] = audio_production_from_name(filename)
        return productions

    def production_date(self, date_fmt=DATE_FORMAT):
        ''' Returns the date for the current month pentaradio as
            string with the format YYYY-MM-DD when no other dateformat is given. '''

        return self.date.strftime(date_fmt)
