#!/usr/bin/env python
# - *- coding: utf- 8 - *-

"""
Collects opera performance data
published on GBOPERA site
"""
import re
import os
import codecs

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "collector"


class Parser(object):

    PAGES_DIR = '/data/pages'
    HEADLINE_FILE = '/data/headline.txt'

    TITLE_PATTERN = '<title>([^<]+?):([^<]+?) | GBOPERA</title>'

    MUSIC_PATTERNS = [
        'Musica di.*?<strong[^>]*?>([^<,&#0-9;]+?)<',
        'Musica di.*?<b[^>]*?>([^<,&#0-9z;]+?)<',
        'Musica di<strong> </strong><strong>([^<]+?)</strong>'
    ]

    CONDUCTOR_PATTERNS = [
        'Direttore<strong> </strong><strong>(.+?)</strong>',
        'Direttore<strong> </strong><strong>([^<]+?)</strong>',
        '> Direttore ([^<]+?)<br />',
        'Direttore</em><strong> </strong><strong>([^<]+?)</strong>',
        'Direttore\W*?<strong> <strong>([^<]+?)</strong>',
        'Direttore<strong> <strong><strong>([^<]+?)</strong>',
        'Direttore.*?<strong[^>]*?>([^<]+?)<',
        'Direttore.*?<b[^>]*?>([^<]+?)<',
    ]

    DIRECTION_PATTERNS = [
        'Regia[^<]*?<strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong>([^<>]{3,50}?) &#8211; <',
        'Regia[^<]*?<b>([^<>]{3,50}?)<',
        'Regia[^<]*?</em>\W*?<strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong[^>]*?>([^<>]{3,50}?)<',
        'Regia[^<]*?<b[^>]*?>([^<>]{3,50}?)<',
        'Regia[^<]*?</span></span><span[^>]*?"><span[^>]*?><b>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong>\W*?<b>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong>\W*?<span[^>]*?>([^<>]{3,50}?)<',
        'Regia[^<]*?</span>\W*?<strong[^>]*?>([^<>]{3,50}?)<',
        'Regia[^<]*?</span>([^<>]{3,50}?)<',
        'Regia[^<]*?<span[^>]*?>\W*?</span><strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<em>\W*?</em>\W*?<strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<span[^>]*?><strong>\W*?</strong></span><strong>([^<>]{3,50}?)<',
        'Regia[^<]*?</span>\W*?<strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong>,</strong> scene, costumi, luci e coreografia  di <strong>([^<>]{3,50}?)<',
        'Regia,</em>\W*?<em>scene, costumi, luci </em><strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<em>([^<>]{3,50}?)<',
        'Regia[^<]*?<em>\W*?</em><strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong>\W*?<strong>([^<>]{3,50}?)<',
        'Regia[^<]*?<strong>\W*?</strong><strong>([^<>]{3,50}?)<',
        'Regia, scene<strong> </strong>e costumi <strong>([^<>]{3,50}?)<'
    ]

    ROLE_LINE_PATTERNS = [
        '>([^<]{3,50}?),\s+?([^<]{3,50}?)<',
        '>([^<]{3,50}?)</em>\s?</em>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</em></span><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?),[^<>]{0,2}?</em></em><em><span[^>]*?>[^<>]{0,50}?</span></em><span[^>]*?>[^<>]{0,2}?([^<]{3,50}?)<',
        '>([^<]{3,50}?),</em><em><span[^>]*?>[^<>]{0,50}?</span></em><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</em><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?),.{0,2}?</em><em><span[^>]*?>[^<]{3,50}?</span></em><em[^>]*?>[^<>]{0,2}?</em><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</span></em><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</span></em><span[^>]*?><span[^>]*?>[^<>]+?</span></span><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</i></span><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</span></strong></em><strong><span[^>]*?>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</span></em><span[^>]*?><span[^>]*?>[^<>]+?</span>([^<]{3,50}?)<',
        '>([^<]{3,50}?)<span[^>]*?>[^<>]+?</span></span></em><span[^>]*?>([^<]{3,50}?)<',
        '>(G[^<]+?)</em><span[^>]*?>[^<>]+?</span>([^<]{3,50}?)<',
        '>([^<]{3,50}?)</em><span[^>]*?>[^<>]+?</span>([^<]{3,50}?)<',
        '<em>([^<]{3,50}?)</em><em>\s+?</em>([^<]{3,50}?)<br />',
        '<em>([^<]{3,50}?)</em>([^<]{3,50}?)<',
        '<i[^>]*?>([^<]{3,50}?)</i>([^<]{3,50}?)</div>',
        '<i>([^<]{3,50}?)</i>([^<]{3,50}?)</span><br />',
        '<br />([^<]{3,50}?)</em>([^<]{3,50}?)<em>',
        '([^<]{3,50}?) </em>([^<]{3,50}?)<',
        '<em><br />([^<]{3,50}?)</em>([^<]{3,50}?)<',
        '>([^<,&#0-9;]{3,50}?)</em><span[^>]*?>([^<,&#0-9;]{3,50}?)<',
        '>\s*?([^<,&#0-9;]+?)<em>\s+?</em>([A-Z\s]{3,50}?[A-Z]{3,50}?)<',
        '>([^<,&#0-9;]{3,50}?</em>\s*?<em>[^<>]{3,50}?)</em>([^<:\*]{3,50}?)<',
        '<em[^>]*?>([^<>]{3,50}?)</em>([^<:\*]{3,50}?)<br />',
        '<i[^>]*?>([^<>]{3,50}?)</i>([^<,&#0-9;]{3,50}?)<br />',
        '<em[^>]*?>([^<>]{3,50}?)</em>([^<,&#0-9;]{2,50}?)</div>',
        '<i>([^<,&#0-9;]{3,50}?)</i>([^<,&#0-9;]{3,50}?)</div>',
        '<br /> (Soprano|Baritono|Tenore) <strong>([^<,&#0-9;]{3,50}?)</strong>',
        '>([^<>]{0,50}?)</em></i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '>([^<>]{0,50}?)</em> </i><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '>([^<>]{0,50}?)</i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,100}?)<',
        '<i><em>([^<>]{0,50}?)</em></i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '<i>([^<>]{0,50}?)</i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '<i><em>([^<>]{0,50}?)</em></i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '<i>([^<>]{0,50}?)</i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '<i>([^<>]{0,50}?)</i></span></span><span[^>]*?><span[^>]*?>([^<a-z,:;\.]{0,50}?)<',
        '>([^>]+?) &#8211; ([^>]+?)<',
        '>([^>]+?) -([^>]+?)<',
        '>\s([A-Z][^<A-Z\s]+[a-z]+)\s([A-Z]{1,3}[^<]{3,50}?)<',
        '>\s([A-Z][^<A-Z\s]+\s[A-Z][^<A-Z\s]+[a-z]+)\s([A-Z]{1,3}[^<]{3,50}?)<',
        '>(\s[A-Z][a-z]+\s[a-z]+\s[A-Z][a-z]+)[^<>A-Z]+?([A-Z]+\s+[^<>]+)<',
        '>([^<,&#0-9;]{3,50}[a-z]+)\s([A-Z\s]{3,50}?[A-Z]{3,50}?)<',
        '>([^<,&#0-9;]{3,50}[a-z]+),\s([A-Z\s]{3,50}?[A-Z]{3,50}?)<',
        '>\s*?([^<,&#0-9;]+?[a-z]+)\s+?([A-Z\s]{3,50}?[A-Z]{3,50}?)<',
    ]

    @staticmethod
    def get_data_dir():
        return os.getcwd() + '/../../'

    @staticmethod
    def parse():
        dir_name = Parser.get_data_dir() + Parser.PAGES_DIR
        count = 0
        for fn in os.listdir(dir_name):
            file_path = dir_name + '/' + fn
            if os.path.isfile(file_path):
                # if fn != '2010_10_teatro-grande-di-brescia-medea_':
                #     continue
                [year, month, _, _] = fn.split('_')
                count += 1
                print(fn)
                fh = codecs.open(file_path, 'r', 'utf-8')
                content = fh.read()
                credit_lines = Parser.parse_credits(content, year, month)
                if len(credit_lines):
                    Parser.write_entry(credit_lines)
                fh.close()

        Parser.write_sorted()
        print(count)

    @staticmethod
    def write_sorted():
        filename = Parser.get_data_dir() + 'data/singer_event/SINGER_EVENT.csv'
        os.system('sort ' + filename + ' -o ' + filename)

    @staticmethod
    def write_entry(entry):
        filename = Parser.get_data_dir() + 'data/singer_event/SINGER_EVENT.csv'
        fh = codecs.open(filename, "a+", 'utf-8')
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
            replace('per la terza volta', ''). \
            replace('il ', ''). \
            replace('Prima mondiale de ', ''). \
            replace(u'La tradizionale modernità di ', ''). \
            replace(u'«Dall’anime esultanti / sboccia l’amor». ', ''). \
            replace('Una', ''). \
            replace('ambientalista', ''). \
            strip("'").\
            strip(" ")

    @staticmethod
    def parse_title(content):
        left_selector, right_selector = '<title>',  '</title>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        title = content[:pos].\
            replace(' | GBOPERA', '').\
            replace('&#8220;', '"').\
            replace('&#8221;', '"').\
            replace('&#8217;', "'"). \
            replace('&#8216;', "'"). \
            replace('&#8211;', "'--").\
            replace('&#8230;', "'..."). \
            replace('&#038;', "&")

        title = Parser.clean(title)

        if ':' in title:
            parts = title.split(':')
            if len(parts) == 2:
                place, name = parts
                return '|'.join([title, Parser.clean(place), Parser.clean(name)])

        for delimiter in [' dal ',
                          ' al ',
                          ' dalla ',
                          ' alla ',
                          ' alle ',
                          ' dall',
                          ' all',
                          ' nella ',
                          ' nel ',
                          ' del ',
                          ' apre ',
                          ' a ']:
            if delimiter in title:
                parts = title.split(delimiter)
                if len(parts) == 2:
                    name, place = parts
                    return '|'.join([title, Parser.clean(place), Parser.clean(name)])

        return '|'.join([title, '-', '-'])

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
    def parse_conductor(content):
        if 'Direttore' not in content:
            return '-'
        for pattern in Parser.CONDUCTOR_PATTERNS:
            pattern = re.compile(pattern)
            match = Parser.clean_name_match(pattern.findall(content))
            if len(match):
                return Parser.format_name_match(match)
        return '-'

    @staticmethod
    def parse_direction(content):
        if 'Regia' not in content:
            return '-'
        for pattern in Parser.DIRECTION_PATTERNS:
            pattern = re.compile(pattern)
            match = Parser.clean_name_match(pattern.findall(content))
            if len(match):
                return Parser.format_name_match(match)
        return '-'

    @staticmethod
    def clean_name_match(match):
        if not len(match):
            return match
        return list(filter(lambda m: len(m) and len(m) < 50,
                           map(lambda m: ' '.join(re.split(r"\s+", m.replace('&#8216;', "'").replace('&#8217;', "'").replace('&#8211;', '').strip(','))).strip(), match)))

    @staticmethod
    def format_name_match(match):
        return ','.join(set([' '.join([w[0].upper() + w[1:].lower() for w in i.replace('  ', ' ').split(' ')]) for i in match]))

    @staticmethod
    def clean_role_match(match):
        if not len(match):
            return []
        cleaned = []
        for (role, name) in match:
            role = Parser.clean_name(role)
            name = Parser.clean_name(name)
            if len(role) and len(name):
                cleaned.append((role, name))
        return cleaned

    @staticmethod
    def clean_name(name):
        return (' '.join(re.split(r"\s+", name))). \
            replace('(13)', ''). \
            replace('(19)', ''). \
            replace('&#8220;', '"'). \
            replace('&#8221;', '"'). \
            replace('&#8217;', "'"). \
            replace('&#8216;', "'"). \
            replace('&#8211;', "'"). \
            replace('&#8230;', "'"). \
            replace('&#038;', "'"). \
            strip(). \
            replace('</em><em>', '').\
            replace(';', ',')

    @staticmethod
    def parse_roles(content, year, month, metadata):
        lines = []
        for pattern in Parser.ROLE_LINE_PATTERNS:
            pattern = re.compile(pattern)
            match = Parser.clean_role_match(pattern.findall(content))
            if len(match):
                for (role, name) in match:
                    if not role.isupper() and role[0].isupper() and name.isupper():
                        print(role + '|' + name)
                        line = '|'.join([year, month, metadata, role, name])
                        if line not in lines:
                            lines.append(line)

        return lines

    @staticmethod
    def parse_credits(content, year, month):
        metadata = Parser.parse_title(content)

        left_selector, right_selector = '<div class="entry-content" itemprop="articleBody" style="color: #363636">',\
                                        '</div><div class="clear"></div>'
        pos = content.index(left_selector)
        content = content[pos + len(left_selector):]
        pos = content.index(right_selector)
        entry = content[:pos]

        metadata += '|' + Parser.parse_music(entry)
        metadata += '|' + Parser.parse_conductor(entry)
        metadata += '|' + Parser.parse_direction(entry)

        if 'Interpreti:' not in content:
            credit_lines = Parser.parse_roles(entry, year, month, metadata)
            if len(credit_lines):
                return '\n'.join(credit_lines)
            else:
                return []

        return []


Parser().parse()