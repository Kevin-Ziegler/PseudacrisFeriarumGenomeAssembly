import pickle


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



numReadsRequired = 3000

# Read the dictionary back from the file
with open("ListDictConnections.pickle", "rb") as file:
	loaded_data = pickle.load(file)
	list2 = loaded_data

dictContigsWithReadsRequired = {}

lstContigsWithReadsRequired = [0]*90000

counter = 0
for i in range(0, len(list2)):
	if len(list2[i]) > 0:
		frequentConnections = FilterDoubleMapped(list2[i], numReadsRequired, i)
		if len(frequentConnections) > 0:
			print("tig000" + str(i) + "_1")
			#for item in frequentConnections:
			#	temp = []
			#	dictContigs[item] = temp
			lstContigsWithReadsRequired[i] = frequentConnections
			for item in frequentConnections:
				name = str(item) + "_" + str(i)
				name2 = str(i) + "_" + str(item)
				dictContigsWithReadsRequired[name] = 1
				dictContigsWithReadsRequired[name2] = 1
			print(frequentConnections)
			#if counter == 100:
			#	break
			counter+=1

for i in range(0, len(lstContigsWithReadsRequired)):
	tempdict = {}
	lstContigsWithReadsRequired[i] = tempdict



listInputFiles = ["HiCToPfer_purged_462_XAZ_DoubleMapped.sam","HiCToPfer_purged_463_XAZ_DoubleMapped.sam","HiCToPfer_purged_464_XAZ_DoubleMapped.sam", "HiCToPfer_purged_465_XAZ_DoubleMapped.sam", "HiCToPfer_purged_466_XAZ_DoubleMapped.sam"]
dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/splits/"



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
		if counter % 1000000 == 0:
			print(counter)

		#if counter == 1000000:
		#	break
		counter+=1

	f.close()


with open("dataCoords.pickle2", "wb") as file:
	pickle.dump(lstContigsWithReadsRequired, file)


counter = 0
for i in range(0, len(lstContigsWithReadsRequired)):
	if len(lstContigsWithReadsRequired[i]) > 0:
		print(i)
		print(lstContigsWithReadsRequired[i])
		counter+=1
		if counter == 1000:
			break



