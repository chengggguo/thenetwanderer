import urllib.request, urllib
import json
from time import sleep
import os

print("in Main api")
url = "https://api.ipplus360.com/ip/geo/v1/street/biz/"
data = {'key':'ijtBb16jOGz0LBkytNWAevtOQc9Wdjuei8dtBpPv6OKxQO4H1LFCoa5wVTRP9J5M','ip':'172.16.100.1','coordsys':'WGS84','area':'multi'}
data = urllib.parse.urlencode(data)
url = url + '?' + data

response = urllib.request.urlopen(url)

data = response.read()
print(data)