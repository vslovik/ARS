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


class Transformer(object):

    EVENTS_FILE = '/data/singer_event/SINGER_EVENT.csv'

    ROLE_GRAPH_FILE = '/data/role_role/multi/ROLE_ROLE.csv'
    SINGER_GRAPH_FILE = '/data/singer_singer/multi/SINGER_SINGER.csv'

    ROLE_GRAPH_FILE_W = '/data/role_role/weighted/ROLE_ROLE.csv'
    SINGER_GRAPH_FILE_W = '/data/singer_singer/weighted/SINGER_SINGER.csv'

    def __init__(self):
        self.meta = dict()

    @staticmethod
    def get_data_dir():
        return os.getcwd() + '/../../'

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
                [_, _, event, theatre, title, composer, conductor, director, role, name] = line.split('|')
                if prev_event == event:
                    event_roles.append(''.join([role, title]))
                    event_names.append('|'.join([name, theatre, title, composer, conductor, director, role]))
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
                    event_roles = []
                    prev_event = event
                    event_names = dict()
        efh.close()
        rfh.close()
        sfh.close()

    def parse_singer(self, half_line):
        items = half_line.split('|')
        singer, meta = items[0], items[1:]
        if singer in meta:
            self.meta[singer].add(meta)
        else:
            self.meta[singer] = set(meta)
        return singer

    def weight_singer_links(self):
        pairs = dict()

        fh = open(Transformer.get_data_dir() + Transformer.SINGER_GRAPH_FILE, 'r')
        with fh as lines:
            for line in lines:
                if not len(line):
                    continue
                this, that = line.split(';')

                pair_key = '|'.join([
                    self.parse_singer(this),
                    self.parse_singer(that)
                ])

                if pair_key in pairs:
                    pairs[pair_key] += 1
                else:
                    pairs[pair_key] = 1
        fh.close()

        fh = open(Transformer.get_data_dir() + Transformer.SINGER_GRAPH_FILE_W, 'r')
        for pair_key, weight in pairs.iteritems():
            this_singer, that_singer = pair_key.split('|')

            fh.write('{0};{1};{2}\n'.format(
                '|'.join([this_singer, '|'.join(sorted(list(self.meta[this_singer])))]),
                '|'.join([that_singer, '|'.join(sorted(list(self.meta[this_singer])))]),
                weight
            ))

        fh.close()

    @staticmethod
    def weight_role_links():
        pairs = dict()

        fh = open(Transformer.get_data_dir() + Transformer.ROLE_GRAPH_FILE, 'r')
        with fh as lines:
            for line in lines:
                if not len(line):
                    continue

                if line in pairs:
                    pairs[line] += 1
                else:
                    pairs[line] = 1
        fh.close()

        fh = open(Transformer.get_data_dir() + Transformer.ROLE_GRAPH_FILE_W, 'r')
        for pair_key, weight in pairs.iteritems():
            this_role, that_role = pair_key.split(';')

            fh.write('{0};{1};{2}\n'.format(
                this_role,
                that_role,
                weight
            ))

        fh.close()

transformer = Transformer()
transformer.events2multi_graphs()
transformer.weight_role_links()
transformer.weight_singer_links()