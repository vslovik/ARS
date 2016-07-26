#!/usr/bin/env python

"""
Transforms edges of multi graph into edges of edge wighted graph
"""
#  Valeriya Slovikovskaya <vslovik@gmail.com>


def parse(input_file, output_file):
    fh = open(output_file, "w")
    with open(input_file, 'r') as lines:
        for line in lines:
            cleaned = line.replace(' Musica di Giacomo Puccini', '')\
                .replace(' Opera in cinque atti, libretto di Luc Bondy, dal dramma omonimo di Arthur Schnitzler.', '')\
                .replace("Melodramma in tre atti su  \\t\\t\\t\\t\\t\\tlibretto di Francesco Maria Piave", '')\
                .replace('Tragedia giapponese in tre atti su Libretto di Luigi Illica e Giuseppe Giacosa','')\
                .replace('Musica di Georg Friedrich Handel', '')\
                .replace('Azione sacra in due parti KV 118, su libretto di Pietro Metastasio', '')
            fh.write(cleaned)
    fh.close()

parse('/home/valerya/project/ars/ARS/docker-python/data/singer_event/singer_event_till2010.csv', '/home/valerya/project/ars/ARS/docker-python/data/singer_event/singer_event_till2010_cleaned.csv')
