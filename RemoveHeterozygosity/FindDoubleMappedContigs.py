#The purpose of this file is to take the dictionary of connection counts from CountDoubleMappedReads.py and filter for contigs pairs which have over a certain number of connections
#A new lst object is created where lst[i] is a dictionary of connections for the ith contig. The key for this dictionary is the number of the contig its connection to and the value is a "coordinate" list of locations where the mappings actually are
#This new data structure is written to disk as outputFrequentCoordinatesLstDict and used later.

import pickle
import sys

#Sam files with only "double mapped reads"
#listInputFiles = ["HiCToPfer_purged_462_XAZ_DoubleMapped.sam","HiCToPfer_purged_463_XAZ_DoubleMapped.sam","HiCToPfer_purged_464_XAZ_DoubleMapped.sam", "HiCToPfer_purged_465_XAZ_DoubleMapped.sam", "HiCToPfer_purged_466_XAZ_DoubleMapped.sam"]
#dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/splits/"
dirc = sys.argv[1]
listInputFiles = sys.argv[2]
listInputFiles = listInputFiles.split(",")

#size of contig list (this value should be larger than the total number of contigs)
#maxContigs = 90000
maxContigs = int(sys.argv[3])

#How many connections are required for there to be a connection worth considering as a heterozygous contig pair
#numReadsRequired = 3000
numReadsRequired = int(sys.argv[4])


#input dictionary from CountDoubleMappedReads.py
inputDictionaryWithConnectionCounts = sys.argv[5]

#Output data structure to be used later
outputFrequentCoordinatesLstDict = sys.argv[6]
#"dataCoords.pickle2"


def FilterDoubleMapped(dict, numreads, contigIndex):
	newdict = {}
	for item in dict:
		if dict[item] > numreads:
			if item != contigIndex:
				newdict[item] = dict[item]
	return newdict


def ParseContigName(tig):
	tig = tig[3:]
	#print(tig)
	number = ""
	flag = 0
	for i in range(0, len(tig)):
		if tig[i] == "_":
			break
		if flag == 1:
			number = number + tig[i]
		if tig[i] == "0":
			flag =1
	return int(number)


def ParseLine(line):
	sline = line.split()
	mapTo = sline[2]
	location1 = sline[3]
	otherMap = ""
	loc2 = ""
	for i in range(0, len(sline)):
		if "XA:Z" in sline[i]:
			otherMap = sline[i][5:]
			temp = ""
			flag_loc2 = 0
			for j in range(0, len(otherMap)):
				if otherMap[j] != "," and flag_loc2 == 0:
					temp = temp + otherMap[j]
				elif flag_loc2 == 0:
					flag_loc2 = 1
				elif flag_loc2 == 1 and otherMap[j] != ",":
					loc2 = loc2 + otherMap[j]
				elif flag_loc2 == 1 and otherMap[j] == ",":
					break
			otherMap = temp
			break
	loc2=loc2[1:]
	return [mapTo, otherMap, int(location1), int(loc2)]



# Read the dictionary back from the file
with open(inputDictionaryWithConnectionCounts, "rb") as file:
	loaded_data = pickle.load(file)
	list2 = loaded_data

dictContigsWithReadsRequired = {}

lstContigsWithReadsRequired = [0]*maxContigs

counter = 0
for i in range(0, len(list2)):
	if len(list2[i]) > 0:
		frequentConnections = FilterDoubleMapped(list2[i], numReadsRequired, i)
		if len(frequentConnections) > 0:
			#print("tig000" + str(i) + "_1")
			#for item in frequentConnections:
			#	temp = []
			#	dictContigs[item] = temp
			lstContigsWithReadsRequired[i] = frequentConnections
			for item in frequentConnections:
				name = str(item) + "_" + str(i)
				name2 = str(i) + "_" + str(item)
				dictContigsWithReadsRequired[name] = 1
				dictContigsWithReadsRequired[name2] = 1
			#print(frequentConnections)
			#if counter == 100:
			#	break
			counter+=1

for i in range(0, len(lstContigsWithReadsRequired)):
	tempdict = {}
	lstContigsWithReadsRequired[i] = tempdict




for item in listInputFiles:
	inputFile = dirc + item

	#inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/splits/HiCToPfer_purged_464_XAZ_DoubleMapped.sam"


	f = open(inputFile, 'r')

	counter = 0

	for line in f:
		templst = ParseLine(line)
		contig1 = ParseContigName(templst[0])
		contig2 = ParseContigName(templst[1])
		if (str(contig1)+"_"+str(contig2)) in dictContigsWithReadsRequired:
			dict1 = lstContigsWithReadsRequired[contig1]
			dict2 = lstContigsWithReadsRequired[contig2]

			if contig2 in dict1:
				dict1[contig2].append(templst[2])
			else:
				dict1[contig2] = [templst[2]]
			if contig1 in dict2:
				dict2[contig1].append(templst[3])
			else:
				dict2[contig1] = [templst[3]]
		#if counter % 1000000 == 0:
			#print(counter)

		#if counter == 1000000:
		#	break
		counter+=1

	f.close()


with open(outputFrequentCoordinatesLstDict, "wb") as file:
	pickle.dump(lstContigsWithReadsRequired, file)
