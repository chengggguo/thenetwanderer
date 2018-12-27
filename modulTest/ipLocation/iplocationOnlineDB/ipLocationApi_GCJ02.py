import urllib.request, urllib
import json
from time import sleep
import os


ipList = open('ipPreSorted.txt','r')
ipLocation = open('ipLocation.txt','w')


iplocation = []
dataJson = []
#innerIsp = {}

counter = 0

######ipplus360 返回数据结构示例
dicStructureSample = {
	"code":200,
	"ip":"101.16.102.110",
	"charge":"true",
	"coordsys":"WGS84",
	"data":{
		"continent":"亚洲",
		"country":"中国",
		"zipcode":"050018",
		"timezone":"UTC+8",
		"accuracy":"区县",
		"owner":"中国联通",
		"correctness":3,
		"consistency":4,
		"multiAreas":[{
			"lat":"38.007994",
			"lng":"114.519142",
			"radius":"",
			"prov":"河北省",
			"city":"石家庄市",
			"district":"裕华区"
			},{
			"lat":"30.007994",
			"lng":"100.519142",
			"radius":"",
			"prov":"北省",
			"city":"家庄市",
			"district":"华区"
			}]
		},
	"msg":"查询成功"
}

def saveJson():

		with open('ipLocation.json','w') as fp:
			json.dump(dataJson,fp,ensure_ascii=False)

		print('free ISP api killed, program shut down at ' + str(counter))
		dataJson.clear()

		ipList.close()
		ipLocation.close()

		os._exit(0)

####call ippuls360 ip locator api and write data into both txt and json files
def ipLocator(i):
	global counter
	print("in Main api")
	url = "https://mall.ipplus360.com/ip/locate/api"
	data = {'key':'ijtBb16jOGz0LBkytNWAevtOQc9Wdjuei8dtBpPv6OKxQO4H1LFCoa5wVTRP9J5M','ip':i,'coordsys':'WGS84','area':'multi'}
	data = urllib.parse.urlencode(data)
	url = url + '?' + data

	response = urllib.request.urlopen(url)

	apicontent = response.read()
	apiDecoded = json.loads(apicontent.decode('utf8'))  ####convert the api result from json string to json dictionary
#	print(apiDecoded)

	innerDic1 = apiDecoded['data']
	innerDic2 = innerDic1['multiAreas']
	print("Main api done")


	try:
		print("in isp api")
		url = "http://api.ipstack.com/"				#### AS and ISP info from ipstack

		ip = i
		data = {"access_key":"a1114497ac70f7e6b6fc2aa0fcd97e1e"}
		data = urllib.parse.urlencode(data)
		url = url + ip + "?" + data

		response = urllib.request.urlopen(url)

		apicontent = response.read()
		ispData = json.loads(apicontent.decode('utf8'))
#		print (ispData)

		innerIsp = ispData['connection']

		asn = innerIsp['asn']
		isp = innerIsp['isp']

		print(asn)
		print(isp)
		print("isp api done")

	except:
		saveJson()


	for n in innerDic2:
		innerDic3 = n



		dataIP={}                                ##### for json
		dataIP['ip'] = apiDecoded['ip']
		dataIP['owner'] = innerDic1['owner']
		dataIP['lat'] = innerDic3['lat']
		dataIP['lng'] = innerDic3['lng']
		dataIP['radius'] = innerDic3['radius']
		dataIP['prov'] = innerDic3['prov']
		dataIP['city'] = innerDic3['city']
		dataIP['district'] = innerDic3['district']
		dataIP['AS'] = innerIsp['asn']
		dataIP['ISP'] = innerIsp['isp']

		a = dataIP['lat']							### baidu map coordys converter. from wgs84 to gcj02
		b = dataIP['lng']

		n = [ ]
		n.append(b)
		n.append(a)
		joinedIP = ','.join(n)


		try:
			print("in baidu api")
			url = "http://api.map.baidu.com/geoconv/v1/"
			data = {'coords':joinedIP,'ak':'Bmq9hUZrLhlDKzyirT76c4YgiuWgRFzi','from':'1','to':'3'} #### from1 = WGS84 from3 = GCJ02 from5 = BD09
			data = urllib.parse.urlencode(data)
			url = url + '?' + data
			resp_text = urllib.request.urlopen(url).read().decode('utf-8')   ####cleaner way

			convertedResult = json.loads(resp_text)				#### loads instead of load here, althtough I don't know why
			convertedInner = convertedResult['result']
			convertedCoordys = convertedInner[0]

			dataIP['lat'] = convertedCoordys['y']
			dataIP['lng'] = convertedCoordys['x']

			print(i + "CoordysConverted")
			print("baidu api done")

		except:
			saveJson()



		print(dataIP)

		sleep(3)

		dataJson.append(dataIP)				#### append all dictionary to dataJson then dump to the .json file by the end of code
		

		iplocation.append(apiDecoded['ip'])     ##### for txt, first coordys in WGS84, second in GCJ02
		iplocation.append(',')
		iplocation.append(innerDic1['owner'])
		iplocation.append(',')		
		iplocation.append(innerDic3['lat'])
		iplocation.append(',')
		iplocation.append(innerDic3['lng'])
		iplocation.append(',')
		iplocation.append(str(dataIP['lat']))
		iplocation.append(',')
		iplocation.append(str(dataIP['lng']))
		iplocation.append(',')
		iplocation.append(str(dataIP['radius']))
		iplocation.append(',')
		iplocation.append(innerDic3['prov'])
		iplocation.append(',')
		iplocation.append(innerDic3['city'])
		iplocation.append(',')
		iplocation.append(innerDic3['district'])
		iplocation.append(',')
		iplocation.append(str(dataIP['AS']))
		iplocation.append(',')
		iplocation.append(dataIP['ISP'])
#		iplocation.append(',')
#		iplocation.append(dataIP['ORG'])
		iplocation.append('\n')
		ipLocation.writelines(iplocation)

		del dataIP
		iplocation.clear()



#	global counter
	counter = counter + 1
	print('no. ' + str(counter) + ' doooooooooooooooooooooooooone')



while True:
	ip = ipList.readline()
	ip = ip.strip()

	if not ip:
		break

	ipLocator(ip)

	with open('ipLocation.json','w') as fp:
		json.dump(dataJson,fp,ensure_ascii=False)  #### ensure_ascii=False -- Chinese can be shown when .json open as txt 

dataJson.clear()

ipList.close()
ipLocation.close()
