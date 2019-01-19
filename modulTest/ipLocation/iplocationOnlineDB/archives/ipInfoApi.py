import urllib.request, urllib
import json


url = "http://api.ipstack.com/"				#### AS and ISP info from ipstack

ip = "110.228.105.17"
data = {"access_key":"096c5b8b3902973393858ef3c7011586"}
data = urllib.parse.urlencode(data)
url = url + ip + "?" + data

response = urllib.request.urlopen(url)

apicontent = response.read()
ispData = json.loads(apicontent.decode('utf8'))
print (ispData)

innerIsp = ispData['connection']

asn = innerIsp['asn']
isp = innerIsp['isp']

print(asn)
print(isp)
