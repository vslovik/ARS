#!/usr/bin/env python
# - *- coding: utf- 8 - *-

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
    TITLE_PATTERN = '<title>(.+)</title>'
    CREDIT_LINE_PATTERNS = ['<br />Musica di.*?<strong>([a-zA-Z\s\/]+[a-zA-Z])?</strong>',
                            '<br />([^<>]+)<b>([a-zA-Z\s\/]+[a-zA-Z])?</b>']
    MUSIC_PATTERNS = [
        'Musica di.*?<strong[^>]*?>([^<]+?)<',
        'Musica di.*?<b[^>]*?>([^<]+?)<',
        'Musica di<strong> </strong><strong>([^<]+?)</strong>'
    ]
    CREDIT_ROLES = ['Musica di', 'Direttore', 'Maestro del Coro', 'Regia', 'Maestro del coro', 'musica di']

    @staticmethod
    def parse():
        dir_name = os.getcwd() + '/../../' + Parser.PAGES_DIR
        count = 0
        for fn in os.listdir(dir_name):
            file_path = dir_name + '/' + fn
            if os.path.isfile(file_path):
                [year, month, _, _] = fn.split('_')
                count += 1
                print(fn)
                fh = open(file_path, "r")
                content = fh.read()
                credit_lines = Parser.parse_credits(content, year, month)
                if len(credit_lines):
                    Parser.write_entry(credit_lines)
                fh.close()
        print(count)

    @staticmethod
    def write_entry(entry):
        filename = os.getcwd() + '/../../' + 'data/singer_event/SINGER_EVENT.csv'
        fh = open(filename, "a+")
        fh.write(entry + '\n')
        fh.close()

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

    @staticmethod
    def remove_html_markup(s):
        tag = False
        quote = False
        out = ""

        for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

        return out

    @staticmethod
    def clean(s):
        return s.\
            replace('ritorna', ''). \
            replace('torna', ''). \
            replace('Torna', ''). \
            replace('chiude la stagione', ''). \
            replace('(cast alternativo)', ''). \
            replace('(ripresa)', ''). \
            replace('inaugura la stagione', ''). \
            replace('trionfano', ''). \
            replace('per la prima volta', ''). \
            replace('diverte il pubblico', ''). \
            replace('Una trionfale', ''). \
            strip("'").\
            strip(" ")

    @staticmethod
    def parse_title(content):
        pattern = re.compile(Parser.TITLE_PATTERN)
        match = pattern.findall(content)
        if len(match):
            title = match[0].replace(' | GBOPERA', '').\
                replace('&#8220;', '"'). \
                replace('&#8221;', '"'). \
                replace('&#8217;', "'")

            has_delimeter = False
            if ':' in title:
                parts = title.split(':')
                if len(parts) == 2:
                    place, name = parts
                    return title + '|' + Parser.clean(place) + '|' + Parser.clean(name)

            if not has_delimeter:
                if 'Messico' not in title:
                    for delimiter in [' dal ', ' al ', ' dalla ', ' alla ', ' alle ',
                                      " dall",  "all'", ' nella ', ' nel ', ' del ',
                                      ' apre ']:
                        if delimiter in title:
                            parts = title.split(delimiter)
                            if len(parts) == 2:
                                name, place = parts
                                if '"' in name and len(name) < 20:
                                    return title + '|' + Parser.clean(place) + '|' + Parser.clean(name)
            return title + '|-|-'

    @staticmethod
    def parse_music(content):
        if 'Musica di' not in content:
            return '-'
        for pattern in Parser.MUSIC_PATTERNS:
            pattern = re.compile(pattern)
            match = Parser.clean_name_match(pattern.findall(content))
            if len(match):
                return Parser.format_name_match(match)
        return '-'

    @staticmethod
    def clean_name_match(match):
        if not len(match):
            return match
        return list(filter(lambda m: len(m) and len(m) < 50, map(lambda m: m.strip(',').strip('\xc2').strip('\xa0').strip(), match)))

    @staticmethod
    def format_name_match(match):
        return ','.join(set([' '.join([w[0].upper() + w[1:].lower() for w in i.split(' ')]) for i in match]))

    @staticmethod
    def parse_credits(content, year, month):
        metadata = year + '|' + month
        metadata += '|' + Parser.parse_title(content)

        left_selector, right_selector = '<div class="entry-content" itemprop="articleBody" style="color: #363636">',\
                                        '</div><div class="clear"></div>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        entry = content[:pos]

        metadata += '|' + Parser.parse_music(entry)

        pattern = re.compile(Parser.ROLE_LINE_PATTERN)
        match = pattern.findall(entry)
        entry_lines = []
        for (role, name) in match:
            role = role.strip('\xc2').strip('\xa0').strip()
            name = name.strip('\xc2').strip('\xa0').strip()
            if len(role) and len(name):
                print('|'.join([role, name]))
                entry_lines.append('|'.join([role, name, metadata]))

        if len(entry_lines):
            return '\n'.join(entry_lines)
        else:
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            return []


Parser().parse()