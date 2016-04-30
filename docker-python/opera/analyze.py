#!/usr/bin/env python

"""
Analyse and visualization of GBOPERA graph
"""
#  Valeriya Slovikovskaya <vslovik@gmail.com>

from analizer import analyzer

analyzer.Analyzer(
    "/vagrant/data/singer_singer/multi/singer_singer.csv",
    "singer_singer",
    "Opera singers connection graph, GBOPERA, 2008-2016",
    False).inform()

analyzer.Analyzer(
    "/vagrant/data/singer_singer/weighted/singer_singer_weighted.csv",
    "singer_singer_weighted",
    "Opera singers weighted connection graph, GBOPERA, 2008-2016",
    True).inform()

analyzer.Analyzer(
    "/vagrant/data/singer_title/multi/singer_title.csv",
    "singer_title",
    "Opera singer vs opera connection graph, GBOPERA, 2008-2016",
    False, True).inform()

analyzer.Analyzer(
    "/vagrant/data/singer_title/weighted/singer_title_weighted.csv",
    "singer_title_weighted",
    "Opera singer vs opera weighted connection graph, GBOPERA, 2008-2016",
    True, True).inform()

analyzer.Analyzer(
    "/vagrant/data/singer_role/multi/singer_role.csv",
    "singer_role",
    "Opera singer vs role connection graph, GBOPERA, 2008-2016",
    False, True).inform()

analyzer.Analyzer(
    "/vagrant/data/singer_role/weighted/singer_role_weighted.csv",
    "singer_role_weighted",
    "Opera singer vs role weighted connection graph, GBOPERA, 2008-2016",
    True, True).inform()



