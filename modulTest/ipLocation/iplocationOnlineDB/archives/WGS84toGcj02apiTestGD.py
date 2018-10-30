import urllib.request, urllib

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


url = "https://restapi.amap.com/v3/assistant/coordinate/convert"
data = {'key':'d47dedc069cc13d93f58827725278d3d','locations':'113.307650,23.120049','coordsys':'baidu'}
data = urllib.parse.urlencode(data)
url = url + '?' + data
#print(url)

response = urllib.request.urlopen(url)

apicontent = response.read()
print(apicontent.decode('utf8'))