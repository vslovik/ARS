#!/usr/bin/env python

"""
Collects opera performance data
published on GBOPERA site
"""
import requests
import re
import time
from html.parser import HTMLParser

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "collector"


class MLStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class Collector(object):

    START_URL = 'http://www.gbopera.it/archives/category/recensioni/page/'
    URL_PATTERN = '(http:\/\/www.gbopera.it\/(\d+\/)+[^\/\d\s&]*\/)'
    CAST_NAME_PATTERN = '[A-Z\s\/]+[A-Z]$'
    SINGER_EVENT_FILE_PATH = '/data/singer_event.csv'

    SINGER_SINGER_FILE_PATH = '/data/singer_singer.csv'
    SINGER_TITLE_FILE_PATH = '/data/singer_title.csv'
    SINGER_ROLE_FILE_PATH = '/data/singer_role.csv'
    MIN_PAGE = 1
    MAX_PAGE = 154

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def grab_archive(self):
        result = range(Collector.MIN_PAGE, Collector.MAX_PAGE)

        # start = random.randrange(Collector.MIN_PAGE, Collector.MAX_PAGE - 5)
        # start = 119
        # result = range(start, start + 5)

        for page in result:
            self.grab_archive_page(page)

    def grab_archive_page(self, page):
        print(page)
        result = requests.get(Collector.START_URL + str(page))
        if 200 != result.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + str(page))
        pattern = re.compile(Collector.URL_PATTERN)
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
        opera_tag = Collector.strip_tags(content.split('<br />')[0].split('CONTATTI')[1].split('</h1></header>')[1]).strip()
        if len(opera_credits):
            self.parse_opera_credits(opera_credits, opera_tag)

    def parse_opera_credits(self, opera_credits, opera_tag):
        line = opera_credits.pop(0)
        title = Collector.strip_tags(line).strip()
        if len(title) == 0:
            return
        pattern = re.compile(Collector.CAST_NAME_PATTERN)
        singer_event_links = []
        singer_title_links = []
        singer_role_links = []
        singers = []

        for line in opera_credits:
            credit = Collector.strip_tags(line).strip()
            match = pattern.findall(credit)
            if len(match) == 0:
                continue
            names = match[0].strip()
            role = credit.replace(names, '').strip()
            for name in names.split(' / '):
                title = title.replace(';', ',')
                if len(title) < 100: # simple way to discard rare parse errors
                    singer_event_links.append('{0}|{1};{2}|{3}\n'.format(name, role, title, opera_tag))
                    singer_title_links.append('{0};{1}\n'.format(name, title))
                    singer_role_links.append('{0};{1}|{2}\n'.format(name, role, title))
                    singers.append(name)
        Collector.write_links(Collector.SINGER_EVENT_FILE_PATH, singer_event_links)
        Collector.write_links(Collector.SINGER_TITLE_FILE_PATH, singer_title_links)
        Collector.write_links(Collector.SINGER_ROLE_FILE_PATH, singer_role_links)
        Collector.write_singers_links(singers)

    @staticmethod
    def write_links(file, links):
        fh = open(file, "a")
        for link in links:
            print(link)
            fh.write(link)
        fh.close()

    @staticmethod
    def write_singers_links(singers):
        singers.sort()
        fh = open(Collector.SINGER_SINGER_FILE_PATH, "a")
        for i in range(0, len(singers) - 2):
            for j in range(i + 1, len(singers) - 1):
                link = '{0};{1}\n'.format(singers[i], singers[j])
                print(link)
                fh.write(link)
        fh.close()