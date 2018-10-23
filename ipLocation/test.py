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

	print(result)
	