#The purpose of this file is to create a dictionary object which contains reads which are mapped to more than one place.
#The input file is a sam file which has been filtered for multimapping reads indicated by XA:Z 
#The output is a binary dictionary which will be used to remove multi mapping reads from the merge no dups file


import pickle
import sys

#dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/"
#dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds/aligned/"
#listInputFiles = ["HiCToPfer_purged_462_XAZ.sam","HiCToPfer_purged_463_XAZ.sam","HiCToPfer_purged_464_XAZ.sam", "HiCToPfer_purged_465_XAZ.sam", "HiCToPfer_purged_466_XAZ.sam"]

#listInputFiles = ["merged_dedup_MultiMap.sam"]
#listInputFiles = ["merged_dedup_ContainsMM.txt"]


#/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds_Try2_4_10_2024/aligned/merged_dedup_Has_XAZ.sam

#dirc = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds_Try2_4_10_2024/aligned/"
#listInputFiles = ["merged_dedup_Has_XAZ.sam"]
#outputDictionary = "MultiMappedReadsHIC_4_10_2024.pickle"

dirc = sys.argv[1]
listInputFiles = sys.argv[2]
outputDictionary = sys.argv[3]


listInputFiles = listInputFiles.split(",")

dictDoubleMappedReads = {}

for item in listInputFiles:
	#print(item)
	f = open(dirc + item, 'r')
	counter = 0
	for line in f:
		sline = line.split()
		if len(sline) > 1:
			readName = sline[0]
			dictDoubleMappedReads[readName] = 1
		if counter % 1000000 == 0:
			#print(counter)
			pass
		counter+=1
	f.close()

#print(dictDoubleMappedReads)


with open(outputDictionary, "wb") as file:
	pickle.dump(dictDoubleMappedReads, file)
