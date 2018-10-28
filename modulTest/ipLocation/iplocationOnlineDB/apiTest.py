#import http.client
import urllib.request, urllib

import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


url = "https://mall.ipplus360.com/ip/locate/api"
data = {'key':'Mmz6TBcuRRkWJh4MHdUeQfC9vym8gBJVJZ8faAKRpQHVZEye3QrKwIYHVDUB14Uo','ip':'223.72.48.58','coordsys':'WGS84','area':'multi'}
data = urllib.parse.urlencode(data)
url = url + '?' + data
#print(url)

response = urllib.request.urlopen(url)

apicontent = response.read()
print(apicontent)