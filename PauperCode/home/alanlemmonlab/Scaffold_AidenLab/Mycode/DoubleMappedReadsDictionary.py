import pickle


#dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/"
dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds/aligned/"
#listInputFiles = ["HiCToPfer_purged_462_XAZ.sam","HiCToPfer_purged_463_XAZ.sam","HiCToPfer_purged_464_XAZ.sam", "HiCToPfer_purged_465_XAZ.sam", "HiCToPfer_purged_466_XAZ.sam"]

#listInputFiles = ["merged_dedup_MultiMap.sam"]
listInputFiles = ["merged_dedup_ContainsMM.txt"]


dictDoubleMappedReads = {}

for item in listInputFiles:
	print(item)
	f = open(dirc + item, 'r')
	counter = 0
	for line in f:
		sline = line.split()
		if len(sline) > 1:
			readName = sline[0]
			dictDoubleMappedReads[readName] = 1
		if counter % 1000000 == 0:
			print(counter)
		counter+=1
	f.close()

#print(dictDoubleMappedReads)


with open("MultiMappedReadsHIC_4_4_2024.pickle", "wb") as file:
	pickle.dump(dictDoubleMappedReads, file)
