#!/usr/bin/env python

"""
Transforms opera performance data
published on GBOPERA site
to further processing
"""
import os

"""www.gbopera.it crawling"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "collector"


class Transformer(object):

    EVENTS_FILE = '/data/singer_event/SINGER_EVENT.csv'

    ROLE_GRAPH_FILE = '/data/role_role/multi/ROLE_ROLE.csv'
    SINGER_GRAPH_FILE = '/data/singer_singer/multi/SINGER_SINGER.csv'

    ROLE_GRAPH_FILE_W = '/data/role_role/weighted/ROLE_ROLE.csv'
    ROLE_DICT = '/data/role_role/weighted/ROLE_DICT.csv'
    SINGER_GRAPH_FILE_W = '/data/singer_singer/weighted/SINGER_SINGER.csv'
    SINGER_DICT = '/data/singer_singer/weighted/SINGER_DICT.csv'

    def __init__(self):
        self.singer_meta = dict()
        self.singer_ids = dict()
        self.role_meta = dict()
        self.role_ids = dict()

    @staticmethod
    def get_data_dir():
        return os.getcwd() + '/../..'

    @staticmethod
    def events2multi_graphs():
        event_roles = []
        event_names = []
        prev_event = None
        efh = open(Transformer.get_data_dir() + Transformer.EVENTS_FILE, "r")
        rfh = open(Transformer.get_data_dir() + Transformer.ROLE_GRAPH_FILE, "w")
        sfh = open(Transformer.get_data_dir() + Transformer.SINGER_GRAPH_FILE, "w")
        with efh as lines:
            for line in lines:
                line = line.strip('\n')
                [_, _, event, theatre, title, composer, conductor, director, role, name] = line.split('|')
                if prev_event == event:
                    event_roles.append('|'.join([role, title]).replace('\n',''))
                    event_names.append('|'.join([name, theatre, title, composer, conductor, director, role]).replace('\n',''))
                else:
                    if len(event_roles) > 0:
                        l = len(event_roles)
                        for i in xrange(0, l):
                            for j in xrange(i + 1, l):
                                rfh.write('{0};{1}\n'.format(event_roles[i], event_roles[j]))
                    if len(event_names) > 0:
                        l = len(event_names)
                        for i in xrange(0, l):
                            for j in xrange(i + 1, l):
                                sfh.write('{0};{1}\n'.format(event_names[i], event_names[j]))
                    prev_event = event
                    event_roles = []
                    event_names = []
        efh.close()
        rfh.close()
        sfh.close()

    def parse_singer(self, half_line):
        items = half_line.split('|')
        singer, meta = items[0], items[1:]
        if singer in self.singer_meta:
            self.singer_meta[singer].update(set(meta))
        else:
            self.singer_meta[singer] = set(meta)
        if singer not in self.singer_ids:
            self.singer_ids[singer] = len(self.singer_ids) + 1
        return self.singer_ids[singer]

    def weight_singer_links(self):
        pairs = dict()

        fh = open(Transformer.get_data_dir() + Transformer.SINGER_GRAPH_FILE, 'r')
        with fh as lines:
            for line in lines:
                line = line.strip('\n')
                if not len(line):
                    continue
                this, that = line.split(';')

                pair_key = '|'.join([
                    str(self.parse_singer(this)),
                    str(self.parse_singer(that))
                ])

                if pair_key in pairs:
                    pairs[pair_key] += 1
                else:
                    pairs[pair_key] = 1
        fh.close()

        fh = open(Transformer.get_data_dir() + Transformer.SINGER_DICT, 'w')
        for singer in self.singer_ids:
            fh.write(
                '|'.join([str(self.singer_ids[singer]), singer, '|'.join(sorted(list(self.singer_meta[singer])))]) + '\n'
            )
        fh.close()

        fh = open(Transformer.get_data_dir() + Transformer.SINGER_GRAPH_FILE_W, 'w')
        for pair_key, weight in pairs.iteritems():
            this_id, that_id = pair_key.split('|')
            fh.write('{0};{1};{2}\n'.format(this_id, that_id, weight))
        fh.close()

    def parse_role(self, half_line):
        items = half_line.split('|')
        role, title = items[0], items[1]
        if role not in self.role_ids:
            self.role_ids[role] = len(self.role_ids) + 1
        if title not in self.role_meta and title != '':
            self.role_meta[role] = title
        return self.role_ids[role]

    def weight_role_links(self):
        pairs = dict()

        fh = open(Transformer.get_data_dir() + Transformer.ROLE_GRAPH_FILE, 'r')
        with fh as lines:
            for line in lines:
                line = line.strip('\n')
                if not len(line):
                    continue
                this, that = line.split(';')

                pair_key = '|'.join([
                    str(self.parse_role(this)),
                    str(self.parse_role(that))
                ])

                if pair_key in pairs:
                    pairs[pair_key] += 1
                else:
                    pairs[pair_key] = 1
        fh.close()

        fh = open(Transformer.get_data_dir() + Transformer.ROLE_DICT, 'w')
        for role in self.role_ids:
            if role in self.role_meta:
                title = self.role_meta[role]
            else:
                title = '-'
            fh.write('|'.join([str(self.role_ids[role]), role, title]) + '\n')
        fh.close()

        fh = open(Transformer.get_data_dir() + Transformer.ROLE_GRAPH_FILE_W, 'w')
        for pair_key, weight in pairs.iteritems():
            this_id, that_id = pair_key.split('|')

            fh.write('{0};{1};{2}\n'.format(
                this_id,
                that_id,
                weight
            ))

        fh.close()

transformer = Transformer()
transformer.events2multi_graphs()
transformer.weight_role_links()
transformer.weight_singer_links()