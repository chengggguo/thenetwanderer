#!/usr/bin/python
#coding:utf-8
#Filename:test.py
#The Program Is Used To Test.

import IPLocate

test = IPLocate.IP()
test.load_dat("/home/db/project/theNetWanderer/offlinedatabase/ipLocationdatabase/IP_trial_2018M09_single_WGS84.dat")
file = open("probers.txt","r")
ipInfo = open("locationAddress.txt","w")
iplocation = []

while True:
	ip = file.readline()

	if not ip:
		break
	result = test.locate_ip(ip)
	print("result start")
	print (result)
	print("result end")

	counter = 5
	while counter <= 12:
		iplocation.append(result[counter])
		iplocation.append(",") #为输出的文档字符间添加空格以供再次split调用

		if counter == 8:
			iplocation.append(result[12])
			iplocation.append(",")
			iplocation.append(result[11])
#			iplocation.append(",")
#			iplocation.append(ip)

		counter+=1

		if counter == 9:
			break

			

	print(ip, "|".join(iplocation))
	ipInfo.writelines(iplocation)
	ipInfo.writelines("\n")
	iplocation = []


file.close()
ipInfo.close()

rFile = open("locationAddress.txt","r") ######去除第一个表中不同ip可能重复的GPS位置
wFile = open("locationAddressSorted.txt","w")

allLine = rFile.readlines()
rFile.close()

s = set()

for i in allLine:
	s.add(i)
for i in s:
	wFile.write(i)
wFile.close()
