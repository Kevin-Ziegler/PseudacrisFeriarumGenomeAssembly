#Suggest joins based on the purge dups overlap file. These regions should overlap and have coverge of a heterozygous sequence. Join the two contigs if they have > threshold hic connections

import pickle

overLapFile = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/purge_dups/dups.bed"
hicDictionaryFile = "HIC_purgedups_Connections.pickle"

canuContigLengths = "/home/alanlemmonlab/Canu_v22_HeterozygousParameters_10_19_2022/CanuContigLengths.txt"
contigLenDict = {}

f = open(canuContigLengths, 'r')


for line in f:
	sline = line.split()
	if len(sline) < 1:
		continue
	contig = sline[0]
	length = sline[1]

	contig = contig[1:]
	length = int(length[4:])
	contigLenDict[contig] = length
f.close()


print(contigLenDict)

hicDictionary = {}

with open(hicDictionaryFile, "rb") as file:
	hicDictionary = pickle.load(file)

#print(hicDictionary)
print("Finished Read")

counter = 0
for item in hicDictionary:
	print(item)
	print(hicDictionary[item])
	if counter == 40:
		break
	counter+=1

f = open(overLapFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 5:
		continue
	if sline[3] == "OVLP":
		print(line)
		smallercontig = sline[0]
		start = sline[1]
		stop = sline[2]
		largercontig = sline[4]
		tempTerm = smallercontig+"_1_"+largercontig+"_1"
		connections = 0

		if tempTerm in hicDictionary:
			connections = hicDictionary[tempTerm]

		if start == "0":
			print("Join: " + largercontig + "_" + smallercontig)
			print("Connections: " + str(connections))

		if stop == str(contigLenDict[smallercontig]):
			print("Join: " + smallercontig + "_" + largercontig)
			print("Connections: " + str(connections))


f.close()
