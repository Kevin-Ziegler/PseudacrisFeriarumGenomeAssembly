inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedHIC/contig_links_iteration_1"
inputLengths = "stats_CHI.txt"

dictLength = {}

f = open(inputLengths, 'r')

for line in f:
	sline = line.split()
	if len(sline) > 0:
		name = sline[0][1:]
		length = int(sline[1])
		dictLength[name] = length
f.close()


f = open(inputFile, 'r')

lstConnections = []
length1 = []
length2 = []

for line in f:
	#print(line)

	sline = line.split()
	if len(sline) > 0:
		name1 = sline[0][:-2]
		name2 = sline[1][:-2]
		con = int(sline[3])
		if name1 in dictLength and name2 in dictLength:
			#print(dictLength.has_key(name2)
			templen1 = dictLength[name1]
			templen2 = dictLength[name2]
			length1.append(templen1)
			length2.append(templen2)
			lstConnections.append(con)



print(lstConnections[:10])
print(length1[:10])
print(length2[:10])

f.close()


lstavg = []

for i in range(0, len(length1)):
	lstavg.append((length1[i]+length2[i])/2)

out = "SizeConnections.txt"
fout = open(out, 'w')

for i in range(0, len(length1)):
	fout.write(str(length1[i]) + " " + str(length2[i]) + " " + str(lstavg[i]) + " " + str(lstConnections[i]) + " \n")
fout.close()


#import matplotlib.pyplot as plt

#l1 = [1, 1, 9, 1, 1, 4, 1, 2, 1]
#l2 = [895437, 621334, 345290, 24161, 284203, 591402, 467145, 284203, 927532]
#l3 = [385851, 101766, 277232, 127517, 260946, 1056899, 81887, 260946, 384865]


#plt.scatter(length1,length2, s = lstConnections)
#plt.show()
#plt.ylabel("Length Scaffold 2")
#plt.xlabel("Length Scaffold 1")
#plt.savefig("ConnectionsBySize.png")
