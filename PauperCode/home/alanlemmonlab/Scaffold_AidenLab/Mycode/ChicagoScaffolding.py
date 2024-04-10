import pickle

pickleFile = "CHI_purgedups_Trimmed_Connections.pickle"
contigsFile = "RepurgedContigLengths_3_29_2024.txt"

outputFileConnectonsGreaterThan10 = "Contig_ContigChicagoConnectonsGreaterThan10.pickle"

dictGreaterThan10 = {}


contigsList = []

f = open(contigsFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 1:
		continue

	contigsList.append(sline[2])

f.close()



chiDict = {}
with open(pickleFile, "rb") as file:
	chiDict = pickle.load(file)

print("read file")


print(chiDict["tig00058886_1_tig00002749_1"])


#print(chiDict["tig00027748_1_tig00066420_1"])
#print(chiDict["tig00000001_1_tig00000006_1_2"])
#print(chiDict["tig00000001_1_tig00000294_1"])
#print(chiDict["tig00000001_1_tig00000334_1"])

connections = 0
connectionsTopTen = 0
minConnections = 8
counter = 0
maxConnections = 100

for item in contigsList:
	print("For Contig:" + item)
	templst = []
	if counter % 10000 == 0:
		print(counter)
	counter +=1

	for item2 in contigsList:

		string = item+"_"+item2
		if string in chiDict:
			temp = []
			#print(string)
			#print(chiDict[string])
			temp.append(item2)
			temp.append(chiDict[string])
			templst.append(temp)
			connections = connections + chiDict[string]

	sortlst = sorted(templst, key=lambda x: x[1])
	if len(sortlst) > 10:
		#print(sortlst[-10:])
		for item3 in sortlst[-10:]:
			connectionsTopTen = connectionsTopTen + item3[1]
	else:
		#print(sortlst)
		for item3 in sortlst:
			connectionsTopTen = connectionsTopTen + item3[1]

	for item2 in sortlst:
		if item2[1] >= minConnections and item2[1] <= maxConnections:
			string = item + "_" + item2[0]
			dictGreaterThan10[string] = 1


print("TotalConnections: " + str(connections))
print("TopTen: " + str(connectionsTopTen))


