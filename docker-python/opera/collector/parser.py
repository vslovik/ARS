#!/usr/bin/env python

"""
Collects opera performance data
published on GBOPERA site
"""
import os

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "collector"

class Parser(object):

    PAGES_DIR = '/data/pages'
    HEADLINE_FILE = '/data/headline.txt'

    @staticmethod
    def parse():
        dir_name = os.getcwd() + '/../../' + Parser.PAGES_DIR
        count = 0
        headlines = []
        for fn in os.listdir(dir_name):
            file_path = dir_name + '/' + fn
            if os.path.isfile(file_path):
                [year, month, _, _] = fn.split('_')
                count += 1
                fh = open(file_path, "r")
                content = fh.read()
                headline = Parser.parse_page(content, year, month)
                fh.close()
                headlines.append(headline)
                break

        headline_file = os.getcwd() + '/../../' + Parser.HEADLINE_FILE
        fh = open(headline_file, "w")
        fh.write("\n".join(headlines))
        fh.close()
        print(count)

    @staticmethod
    def parse_page(content, year, month):
        headline = Parser.parse_headline(content, year, month)
        entry = Parser.parse_credits(content)
        print(entry)
        return headline

    @staticmethod
    def parse_headline(content, year, month):
        left_selector, right_selector = '<header class="entry-header">',  '</header>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        headline = year + '|' + month  + '|' +  content[:pos].\
            replace('<h1 class="entry-title" itemprop="name">', '').\
            replace('</h1>', '').\
            replace('&#8220;', '"').\
            replace('&#8221;', '"').\
            replace('&#8217;', "'")

        return headline

    @staticmethod
    def parse_credits(content):
        left_selector, right_selector = '<div class="entry-content" itemprop="articleBody" style="color: #363636">',\
                                        '</div><div class="clear"></div>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        entry = content[:pos]

        return entry

Parser.parse()