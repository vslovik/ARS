#!/usr/bin/env python

"""
Collects opera performance data
published on GBOPERA site
"""
#  Valeriya Slovikovskaya <vslovik@gmail.com>


def weight(input_file, output_file):
    items = dict()
    with open(input_file, 'r') as lines:
        for line in lines:
            line = line.rstrip()
            if items.has_key(line):
                items[line] += 1
            else:
                items[line] = 1
    fh = open(output_file, "w")
    for key, value in items.iteritems():
        fh.write('{0};{1}\n'.format(key,value))
    fh.close()

weight('/vagrant/data/singer_singer.csv','/vagrant/data/singer_singer_weighted.csv')
weight('/vagrant/data/singer_title.csv','/vagrant/data/singer_title_weighted.csv')
weight('/vagrant/data/singer_role.csv','/vagrant/data/singer_role_weighted.csv')