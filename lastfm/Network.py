__author__ = 'Giulio Rossetti'
__license__ = "GPL"
__email__ = "giulio.rossetti@gmail.com"

# register a valid API-KEY at the following url:
# http://www.lastfm.it/api

from lastfm import api
import os


def get_friends(api, username, c):
    user = api.get_user(username)
    ff = user.get_friends()
    c += 1
    return ff, c


api_key = "2e8e6091dbf709e685740dc8987ff657"
seed = "Pusho87"

api_u = api.Api(api_key)

seen = {}
user_list = [seed]
count = 0
max_users = 5000

out = open("network.csv", "w")

while count < max_users:
     try:
        friends, count = get_friends(api_u, user_list[count], count)
        print count-1, user_list[count-1]
        for f in friends:
            fname = f.name
            res = "%s,%s\n" % (user_list[count-1], fname)
            out.write("%s" % res.encode('utf-8'))
            if fname not in seen:
                seen[fname] = None
                user_list.append(fname)
            out.flush()
     except:
         pass

out.close()