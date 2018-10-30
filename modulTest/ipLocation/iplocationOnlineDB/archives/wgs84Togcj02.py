import json

import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def transformlat(lat,lng):

	ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
		0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
	ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
		math.sin(2.0 * lng * pi)) * 2.0 / 3.0
	ret += (20.0 * math.sin(lat * pi) + 40.0 *
		math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
	ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
		math.sin(lat * pi / 30.0)) * 2.0 / 3.0
	return ret


def transformlng(lat,lng):
	ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
		0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
	ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
		math.sin(2.0 * lng * pi)) * 2.0 / 3.0
	ret += (20.0 * math.sin(lng * pi) + 40.0 *
		math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
	ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
		math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
	return ret
 

def out_of_china(lat,lng):

	if lng < 72.004 or lng > 137.8347:
		return True
	if lat < 0.8293 or lat > 55.8271:
		return True
	return False



def wgs84togcj02(lat,lng):	

	if out_of_china(lat, lng):
		return lat, lng

	dlat = transformlat(lng - 105.0, lat - 35.0)
	dlng = transformlng(lng - 105.0, lat - 35.0)
	radlat = lat / 180.0 * pi
	magic = math.sin(radlat)
	magic = 1 - ee * magic * magic
	sqrtmagic = math.sqrt(magic)
	dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
	dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
	mglat = lat + dlat
	mglng = lng + dlng
	return [mglat, mglng]


if __name__ == '__main__':
	lng = 121.543
	lat = 31.065
	result3 = wgs84togcj02(lat, lng)
	print(result3)

