#!/usr/bin/env python
import requests
import re

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "opera"


class Api(object):

    START_URL = 'http://www.gbopera.it/archives/category/recensioni/'
    URL_PATTERN = '(http:\/\/www.gbopera.it\/(\d+\/)+[^\/\d]+\/)'

    def get_event(self, opera, composer, theatre, year):

        """
        Grab event.

        @param opera     opera
        @type opera:     L{str}
        @param composer: composer
        @type composer:  L{str}
        @param theatre:  theatre
        @type theatre:   L{str}
        @param year:     year
        @type year:      L{str}

        @return:         void

        """
        r = requests.get(self.START_URL)

        if 200 != r.status_code:
            raise ConnectionError('Can not gran gbopera page')

        c = str(r.content)[0:20000]

        p = re.compile(self.URL_PATTERN)
        m = p.findall(c)

        print(m)