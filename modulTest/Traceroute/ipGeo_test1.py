import urllib.request, urllib
import json
from time import sleep
import os

print("in Main api")
url = "https://mall.ipplus360.com/ip/locate/api"
data = {'key':'','ip':i,'coordsys':'WGS84','area':'multi'}
data = urllib.parse.urlencode(data)
url = url + '?' + data

response = urllib.request.urlopen(url)

apicontent = response.read()