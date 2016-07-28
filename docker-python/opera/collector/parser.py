#!/usr/bin/env python

"""
Collects opera performance data
published on GBOPERA site
"""
import re
import os

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "collector"


class Parser(object):

    PAGES_DIR = '/data/pages'
    HEADLINE_FILE = '/data/headline.txt'

    ROLE_LINE_PATTERN = '<em>([^<>]+?)</em>([A-Z\s\/]+[A-Z])<br />'
    TITLE_PATTERN = '<br />[^<>]+<strong>([A-Z\s\/]+[A-Z])?</strong>'
    CREDIT_LINE_PATTERNS = ['<br />([^<>]+)<strong>([a-zA-Z\s\/]+[a-zA-Z])?</strong>',
                            '<br />([^<>]+)<b>([a-zA-Z\s\/]+[a-zA-Z])?</b>']
    CREDIT_ROLES = ['Musica di', 'Direttore', 'Maestro del Coro', 'Regia', 'Maestro del coro', 'musica di']

    def __init__(self):
        self.roles = set([])

    def parse(self):
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
                headline = self.parse_page(content, year, month)
                fh.close()
                headlines.append(headline)

        headline_file = os.getcwd() + '/../../' + Parser.HEADLINE_FILE
        fh = open(headline_file, "w")
        fh.write("\n".join(headlines))
        fh.close()
        print(count)

    def parse_page(self, content, year, month):
        headline = Parser.parse_headline(content, year, month)
        entry = self.parse_credits(content, year)
        return headline

    @staticmethod
    def parse_headline(content, year, month):
        left_selector, right_selector = '<header class="entry-header">',  '</header>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        headline = year + '|' + month + '|' + content[:pos].\
            replace('<h1 class="entry-title" itemprop="name">', '').\
            replace('</h1>', '').\
            replace('&#8220;', '"').\
            replace('&#8221;', '"').\
            replace('&#8217;', "'")

        return headline

    def parse_credits(self, content, year):
        left_selector, right_selector = '<div class="entry-content" itemprop="articleBody" style="color: #363636">',\
                                        '</div><div class="clear"></div>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        entry = content[:pos]

        pattern = re.compile(Parser.ROLE_LINE_PATTERN)
        match = pattern.findall(entry)
        for (role, name) in match:
            print(role.strip() + '|' + name.strip() + '\n')

        matches = []
        for item in Parser.CREDIT_LINE_PATTERNS:
            pattern = re.compile(item)
            matches.append(pattern.findall(entry))

        for match in matches:
            for (role, name) in match:
                r = role.replace('&nbsp;', ' ').strip()
                if r in Parser.CREDIT_ROLES:
                    print(r + '|' + name)

        return entry


Parser().parse()