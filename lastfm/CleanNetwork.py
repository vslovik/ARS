__author__ = 'rossetti'
__license__ = "GPL"
__email__ = "giulio.rossetti@gmail.com"

import os

f = open("data%snetwork.csv" % os.sep)
out = open("data%snetwork_cleaned.csv" % os.sep, "w")
ouu = open("data%susers.csv" % os.sep, "w")

users = {}
for l in f:
    users[l.split(",")[0]] = None

f = open("data%snetwork.csv" % os.sep)
for l in f:
    u = l.rstrip().split(",")
    if u[0] in users and u[1] in users:
        out.write(l)
out.flush()
out.close()

for u in users:
    ouu.write("%s\n" % u)
ouu.flush()
ouu.close()