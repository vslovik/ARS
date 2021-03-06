#!/usr/bin/env python

"""
Grabs opera performance data
published on GBOPERA site
"""
import requests
import re
import time
import os
import codecs

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"


class Grabber(object):

    ENCODING = 'utf-8'
    START_URL = 'http://www.gbopera.it/archives/category/recensioni/page/'
    URL_PATTERN = '(http:\/\/www.gbopera.it\/(\d+\/)+[^\/\d\s&]*\/)'
    MIN_PAGE = 1
    MAX_PAGE = 1000

    @staticmethod
    def get_pages_dir():
        return os.getcwd() + '/data/pages/'

    @staticmethod
    def grab_archive():
        result = range(Grabber.MIN_PAGE, Grabber.MAX_PAGE)
        for page in result:
            Grabber.grab_archive_page(page)

    @staticmethod
    def grab_archive_page(page):
        print(page)
        result = requests.get(Grabber.START_URL + str(page))
        if 200 != result.status_code:
            raise Exception('Can not grab gbopera page: ' + str(page))
        result.encoding = 'utf-8'
        pattern = re.compile(Grabber.URL_PATTERN)
        match = pattern.findall(result.text.encode('utf-8'))
        for x in set(match):
            Grabber.grab_event_page(x[0])

    @staticmethod
    def grab_event_page(url):
        time.sleep(1)
        print(url)
        result = requests.get(url)
        if 200 != result.status_code:
            raise Exception('Can not grab gbopera page: ' + url)
        result.encoding = 'utf-8'
        filename = Grabber.get_pages_dir() + url.replace('http://www.gbopera.it/', '').replace('/', '_')
        fh = codecs.open(filename, 'w', 'utf-8')
        fh.write(result.text)
        fh.close()

Grabber.grab_archive()