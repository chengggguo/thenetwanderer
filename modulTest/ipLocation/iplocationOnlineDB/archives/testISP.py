import urllib.request, urllib
import json
from time import sleep
counter = 0

while 1:

	url = "http://ip-api.com/json/"
	data = '101.95.236.117'
#data = urllib.parse.urlencode(data)
	url = url + data
#print(url)

	response = urllib.request.urlopen(url)

	apicontent = response.read()
	print(apicontent.decode('utf8'))

	isp = json.loads(apicontent)
	sleep(12)
	counter = counter +1
	print(counter)


