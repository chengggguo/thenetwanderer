import urllib.request, urllib
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context

ipList = open('ipPreSorted.txt','r')
ipLocation = open('ipLocation.txt','w')


iplocation = []
dataJson = []

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

def writeToJsonFile(path,fileName,data):
	filePathNameWExt = './'+ path + '/' + fileName + '.json'
	with open(filePathNameWExt,'w') as fp:
		json.dump(data,fp)

####call ippuls360 ip locator api and write data into both txt and json files
def ipLocator(i):
	url = "https://mall.ipplus360.com/ip/locate/api"
	data = {'key':'m00oHrSRYKKDPiRvPHhndGnh2cgouMWzQsudsVpwSx5Lg7pImB96pbVbHi3CZ1RJ','ip':i,'coordsys':'WGS84','area':'multi'}
	data = urllib.parse.urlencode(data)
	url = url + '?' + data
#	print(i)
#	print('api called')

	response = urllib.request.urlopen(url)

	apicontent = response.read()
	apiDecoded = json.loads(apicontent.decode('utf8'))  ####convert the api result from json string to json dictionary
	print(apiDecoded)
	innerDic1 = apiDecoded['data']
	innerDic2 = innerDic1['multiAreas']


#	print(innerDic2)

	for i in innerDic2:
		iplocation.append(apiDecoded['ip'])     ##### for txt
		iplocation.append(',')
		iplocation.append(innerDic1['owner'])
		iplocation.append(',')
#		print(i)
		innerDic3 = i
#		print(innerDic3['lng'])
		iplocation.append(innerDic3['lat'])
		iplocation.append(',')
		iplocation.append(innerDic3['lng'])
		iplocation.append(',')
		iplocation.append(innerDic3['prov'])
		iplocation.append(',')
		iplocation.append(innerDic3['city'])
		iplocation.append(',')
		iplocation.append(innerDic3['district'])
		iplocation.append('\n')
		print(iplocation)
		ipLocation.writelines(iplocation)

		iplocation.clear()

		data={}                                ##### for json
		data['ip'] = apiDecoded['ip']
		data['owner'] = innerDic1['owner']
		data['lat'] = innerDic3['lat']
		data['lng'] = innerDic3['lng']
		data['prov'] = innerDic3['prov']
		data['city'] = innerDic3['city']
		data['district'] = innerDic3['district']

		dataJson.append(data)
		del data








while True:
	ip = ipList.readline()
	ip = ip.strip()

	if not ip:
		break

	ipLocator(ip)

	with open('ipLocation.json','w') as fp:
		json.dump(dataJson,fp)

dataJson.clear()

ipList.close()
ipLocation.close()





