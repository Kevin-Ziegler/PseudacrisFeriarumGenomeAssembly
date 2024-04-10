import pickle


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
	otherMap = ""
	for i in range(0, len(sline)):
		if "XA:Z" in sline[i]:
			otherMap = sline[i][5:]
			temp = ""
			for j in range(0, len(otherMap)):
				if otherMap[j] != ",":
					temp = temp + otherMap[j]
				else:
					break
			otherMap = temp
			break
	return mapTo, otherMap



listInputFiles = ["HiCToPfer_purged_462_XAZ_DoubleMapped.sam","HiCToPfer_purged_463_XAZ_DoubleMapped.sam","HiCToPfer_purged_464_XAZ_DoubleMapped.sam", "HiCToPfer_purged_465_XAZ_DoubleMapped.sam", "HiCToPfer_purged_466_XAZ_DoubleMapped.sam"]
dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/splits/"


list = []

for i in range(0, 90000):
	temp = {}
	list.append(temp)



for item in listInputFiles:
	inputFile = dirc + item
	print(item)


	f = open(inputFile, 'r')
	counter = 0

	for line in f:
		contig1, contig2  = ParseLine(line)
		#print(contig1, contig2)
		contignumber1 = ParseContigName(contig1)
		contignumber2 = ParseContigName(contig2)
		#print(contignumber1, contignumber2)
		if contignumber1 in list[contignumber2]:
			list[contignumber2][contignumber1]+=1
		else:
			list[contignumber2][contignumber1] = 1
		if contignumber2 in list[contignumber1]:
			list[contignumber1][contignumber2]+=1
		else:
			list[contignumber1][contignumber2] = 1

		if counter % 1000000 == 0:
			print(counter)

		#if counter == 100000:
		#	break
		counter+=1





	f.close()

# Save the dictionary to a file
with open("data.pickle2", "wb") as file:
	pickle.dump(list, file)

# Read the dictionary back from the file
with open("data.pickle2", "rb") as file:
	loaded_data = pickle.load(file)
	#list2 = loaded_data

"""
for i in range(0, len(list2)):
	if len(list2[i]) > 0:
		print("tig000" + str(i) + "_1")
		print(list2[i])
"""
