#!/usr/bin/env python

"""
Collects opera performance data
published on GBOPERA site
"""
#  Valeriya Slovikovskaya <vslovik@gmail.com>

from collector import collector

collector.Collector.grab_archive(collector.Collector())