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
    SINGER_EVENT_FILE_PATH = '/data/singer_event.csv'
    SINGER_SINGER_FILE_PATH = '/data/singer_singer.csv'
    MIN_PAGE = 1
    MAX_PAGE = 154

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def grab_archive(self):
        result = range(Api.MIN_PAGE, Api.MAX_PAGE)
        for page in result:
            self.grab_archive_page(page)

    def grab_archive_page(self, page):
        print(page)
        result = requests.get(Api.START_URL + str(page))
        if 200 != result.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + str(page))
        pattern = re.compile(Api.URL_PATTERN)
        match = pattern.findall(str(result.content)[0:])
        for x in set(match):
            self.grab_event_page(x[0])

    def grab_event_page(self, url):
        time.sleep(1)
        print(url)
        result = requests.get(url)
        if 200 != result.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + url)
        self.parse_content(str(result.content.decode('ascii', 'ignore').encode('ascii'))[0:])

    def parse_content(self, content):
        # filter opera credits
        opera_credits = list(filter(lambda x: 0 < len(x.strip()) < 500, content.split('<br />')))
        opera_tag = Api.strip_tags(content.split('<br />')[0].split('CONTATTI')[1].split('</h1></header>')[1]).strip()
        if len(opera_credits):
            self.parse_opera_credits(opera_credits, opera_tag)

    def parse_opera_credits(self, opera_credits, opera_tag):
        line = opera_credits.pop(0)
        title = Api.strip_tags(line).strip()
        if len(title) == 0:
            return
        pattern = re.compile(Api.CAST_NAME_PATTERN)
        singer_event_links = []
        singers = []
        for line in opera_credits:
            credit = Api.strip_tags(line).strip()
            match = pattern.findall(credit)
            if len(match) == 0:
                continue
            names = match[0].strip()
            role = credit.replace(names, '').strip()
            for name in names.split(' / '):
                singer_event_links.append('"{0}|{1}","{2}|{3}"\n'.format(name, role, title, opera_tag))
                singers.append(name)
        Api.write_singer_event_links(singer_event_links)
        Api.write_singers_links(singers)

    @staticmethod
    def write_singer_event_links(singer_event_links):
        fh = open(Api.SINGER_EVENT_FILE_PATH, "a")
        for link in singer_event_links:
            print(link)
            fh.write(link)
        fh.close()

    @staticmethod
    def write_singers_links(singers):
        fh = open(Api.SINGER_SINGER_FILE_PATH, "a")
        for name in singers:
            for other_name in singers:
                if name != other_name:
                    link = '"{0}","{1}"\n'.format(name, other_name)
                    print(link)
                    fh.write(link)
        fh.close()