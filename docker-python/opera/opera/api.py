#!/usr/bin/env python
import requests
import re
import time
import random
from html.parser import HTMLParser

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "opera"


class MLStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class Api(object):

    START_URL = 'http://www.gbopera.it/archives/category/recensioni/page/'
    URL_PATTERN = '(http:\/\/www.gbopera.it\/(\d+\/)+[^\/\d\s&]*\/)'
    CAST_NAME_PATTERN = '[A-Z\s\/]+[A-Z]$'
    MIN_PAGE = 1
    MAX_PAGE = 154

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def grab_archive(self):

        start = self.MIN_PAGE
        end = self.MAX_PAGE
        r = range(self.MIN_PAGE, self.MAX_PAGE)

        start = random.randrange(self.MIN_PAGE, self.MAX_PAGE - 5)
        start = 119
        r = range(start, start + 5)

        for page in r:
            self.grab_archive_page(page)

    def grab_archive_page(self, page):

        print(page)
        r = requests.get(self.START_URL + str(page))

        if 200 != r.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + str(page))

        c = str(r.content)[0:]

        p = re.compile(self.URL_PATTERN)
        m = p.findall(c)

        for x in set(m):
            self.grab_event_page(x[0])

    def grab_event_page(self, url):

        #time.sleep(1)
        print(url)
        r = requests.get(url)

        if 200 != r.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + url)

        content = str(r.content.decode('ascii', 'ignore').encode('ascii'))[0:]

        # filter opera credits
        opera_credits = list(filter(lambda x: 0 < len(x.strip()) < 500, content.split('<br />')))

        opera_tag = Api.strip_tags(content.split('<br />')[0].split('CONTATTI')[1].split('</h1></header>')[1]).strip()

        p = re.compile(self.CAST_NAME_PATTERN)

        title = ''
        first = True
        for line in opera_credits:
            t = Api.strip_tags(line).strip()
            if first:
                if len(t) == 0:
                    break
                title = t
                first = False
            else:
                m = p.findall(t)
                if len(m):
                    names = m[0].strip()
                    if len(names) > 1:
                        role = t.replace(names, '').strip()
                        for name in names.split(' / '):
                            print("'" + name + '|' + role + "','" + title + '|' + opera_tag + "'")
