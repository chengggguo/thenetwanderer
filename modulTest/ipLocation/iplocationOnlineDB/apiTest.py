#import http.client
import urllib.request, urllib

import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


url = "https://mall.ipplus360.com/ip/locate/api"
data = {'key':'fRQk7uOaZZbZ1pZD8A5WmYQ5fXsTpitcbtgA7v6y8V6qXn82G6M4fIyoxzXwtljk','ip':'223.72.48.58','coordsys':'BD09','area':'multi'}
data = urllib.parse.urlencode(data)
url = url + '?' + data
print(url)

response = urllib.request.urlopen(url)

apicontent = response.read()
print(apicontent)