import urllib.request, urllib

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


url = "https://mall.ipplus360.com/ip/locate/api"
data = {'key':'m00oHrSRYKKDPiRvPHhndGnh2cgouMWzQsudsVpwSx5Lg7pImB96pbVbHi3CZ1RJ','ip':'202.97.89.133','coordsys':'WGS84','area':'multi'}
data = urllib.parse.urlencode(data)
url = url + '?' + data
#print(url)

response = urllib.request.urlopen(url)

apicontent = response.read()
print(apicontent.decode('utf8'))