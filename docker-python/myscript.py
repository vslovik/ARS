import requests
import pprint
import re

r = requests.get('http://google.com')
print(r.status_code)

# https://pythonprogramming.net/urllib-tutorial-python-3/)

r = requests.get('http://www.gbopera.it/archives/category/recensioni/')
print(r.url);

print(r.status_code);
print(r.encoding);
print(r.status_code);

c = str(r.content)[0:20000]

print(c);
#print(r.content);

p = re.compile('http:\/\/www.gbopera.it\/2016\/04\/[^\/\d]+\/')

p = re.compile('(http:\/\/www.gbopera.it\/(\d+\/)+[^\/\d]+\/)')

m = p.findall(c)
print(m)

#r = requests.get('http://www.gbopera.it/archives/category/recensioni/', stream=True)

#print(r.raw.read(10))
#pprint.pprint(globals())
#pprint.pprint(locals())
#</em>FRANCESCO PITTARI<br />
#http://www.gbopera.it/2016/