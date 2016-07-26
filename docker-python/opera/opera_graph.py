#!/usr/bin/env python

"""
Transforms edges of multi graph into edges of edge wighted graph
"""
#  Valeriya Slovikovskaya <vslovik@gmail.com>


def parse(input_file, output_file):
    event_roles = []
    fh = open(output_file, "w")
    with open(input_file, 'r') as lines:
        prev_event = ''
        for line in lines:
            line = line.rstrip()
            if line.find(';') == -1 or line.count(';') > 1:
                continue
            [singer, event] = line.split(';')
            if singer.find('|') == -1 or event.find('|') == -1 or singer.count('|') > 1 or event.count('|') > 1:
                continue
            [name, role] = singer.split('|')
            [title, details] = event.split('|')
            if prev_event == event:
                event_roles.append(role + '|' + title)
            else:
                if len(event_roles) > 0:
                    l = len(event_roles)
                    for i in xrange(0, l):
                        for j in xrange(i + 1, l):
                            fh.write('{0};{1}\n'.format(event_roles[i], event_roles[j]))
                event_roles = []
                prev_event = event
    fh.close()

parse('/home/valerya/project/ars/ARS/docker-python/data/singer_event/singer_event_till2010.csv', '/home/valerya/project/ars/ARS/docker-python/data/singer_event/opera.csv')
