#!/usr/bin/env python

"""
Collects opera performance data
published on GBOPERA site
"""
import requests
import re
import time

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "collector"

class Grabber(object):

    START_URL = 'http://www.gbopera.it/archives/category/recensioni/page/'
    URL_PATTERN = '(http:\/\/www.gbopera.it\/(\d+\/)+[^\/\d\s&]*\/)'
    MIN_PAGE = 1
    MAX_PAGE = 1000

    def grab_archive(self):
        result = range(Grabber.MIN_PAGE, Grabber.MAX_PAGE)
        for page in result:
            self.grab_archive_page(page)

    def grab_archive_page(self, page):
        print(page)
        result = requests.get(Grabber.START_URL + str(page))
        if 200 != result.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + str(page))
        pattern = re.compile(Grabber.URL_PATTERN)
        match = pattern.findall(str(result.content)[0:])
        for x in set(match):
            self.grab_event_page(x[0])

    def grab_event_page(self, url):
        time.sleep(1)
        print(url)
        result = requests.get(url)
        if 200 != result.status_code:
            raise ConnectionError('Can not grab gbopera page: ' + url)
        content = str(result.content.decode('ascii', 'ignore').encode('ascii'))[0:]
        filename = '/data/pages/' + url.replace('http://www.gbopera.it/', '').replace('/', '_')
        fh = open(filename, "w")
        fh.write(content)
        fh.close()