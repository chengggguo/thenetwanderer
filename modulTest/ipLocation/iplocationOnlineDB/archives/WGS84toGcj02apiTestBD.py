import urllib.request, urllib
import json


url = "http://api.map.baidu.com/geoconv/v1/"
data = {'coords':'113.307650,23.120049','ak':'Bmq9hUZrLhlDKzyirT76c4YgiuWgRFzi','from':'5','to':'3'} #### from1 = WGS84 from3 = GCJ02 from5 = BD09
data = urllib.parse.urlencode(data)
url = url + '?' + data
#print(url)

response = urllib.request.urlopen(url)

apicontent = response.read()
print(apicontent.decode('utf8'))

sss = json.loads(apicontent)

