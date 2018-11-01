#!/usr/bin/python
#coding:utf-8
#Filename:test.py
#The Program Is Used To Test.

import IPLocate

test = IPLocate.IP()
test.load_dat("/home/db/project/theNetWanderer/offlinedatabase/ipLocationdatabase/IP_trial_2018M09_single_WGS84.dat") ##### wrong path
file = open("probers.txt","r")
#ipInfo = open("locationAddress.txt","w")
wFile = open("ipPreSorted.txt","w")
iplocation = []

bo = 1
lauNew = ''
lauOld = ''
lauOldIp = ''

while True:
	ip = file.readline()

	if not ip:
		break
	result = test.locate_ip(ip)
#	print("result start")
#	print (result)
#	print("result end")

	counter = 5
	while counter <= 12:
		iplocation.append(result[counter])
#		iplocation.append(",") #为输出的文档字符间添加空格以供再次split调用

		if counter == 8:                         # 修改经纬度顺序，以供调用
			iplocation.append(result[12])
#			iplocation.append(",")
			iplocation.append(result[11])
#			iplocation.append(",")
			iplocation.append(ip)

		counter+=1

		if counter == 9:
			break

			
	print(iplocation)
	lauNew = iplocation[4]
	if bo == 1:
		lauOld = iplocation[4]
		lauOldIp = iplocation[6]

		bo = 0

	if bo == 0:
		if lauNew != lauOld:
			wFile.writelines(lauOldIp)
			print(lauNew)
			print(lauOld)

			bo = 1
	else:
		pass


	iplocation = []

wFile.close()
file.close()

		





#	print(ip, "|".join(iplocation))
#	ipInfo.writelines(iplocation)
#	ipInfo.writelines("\n")
#	iplocation = []


#file.close()
#ipInfo.close()

#rFile = open("locationAddress.txt","r") ######去除第一个表中不同ip可能重复的GPS位置
#wFile = open("ipPreSort.txt","w")
#info = []
#with open("locationAddress.txt","r") as fh:
#	line = fh.readline()

#	while line:
#		info = line.split()
#		print(info)
#		line = fh.readline()





#rFile.close()

#s = set()

#for i in allLine:
#	s.add(i)
#for i in s:
#	wFile.write(i)
#wFile.close()
