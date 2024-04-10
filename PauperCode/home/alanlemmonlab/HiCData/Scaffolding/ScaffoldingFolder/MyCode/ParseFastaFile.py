#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedHIC/scaffolds_FINAL.fasta"
#outputFile = "stats_HIC.txt"
#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedChicago/scaffolds_FINAL.fasta"
#inputFile = "/home/alanlemmonlab/HiCData/Scaffolding/ScaffoldingFolder/mapping_pipeline/PurgedChicago_v2/scaffolds_FINAL.fasta"
#outputFile = "stats_clip_Chi_v2.txt"

#inputFile = "/home/alanlemmonlab/HiCData/Scaffolding/ScaffoldingFolder/mapping_pipeline/PurgedChicago_v2_GATC/scaffolds_FINAL.fasta"
#inputFile = "/home/alanlemmonlab/HiCData/Scaffolding/ScaffoldingFolder/mapping_pipeline/Purged_HIC_v2_GATC/scaffolds_FINAL.fasta"
#outputFile = "stats_clip_HIC_GATC_v2.txt"


#inputFile = "/home/alanlemmonlab/TryArrow2/myConsensus.fasta"
#outputFile = "stats_polished.txt"

inputFile = "/home/alanlemmonlab/Canu_v22_HeterozygousParameters_10_19_2022/P_fer_HeterozygousParameters.contigs.fasta"
outputFile = "stats_Canu_v2.txt"


f = open(inputFile, 'r')
fout = open(outputFile, 'w')

lstLineLengths = []
countScaffolds = 0
currentBP = 0
numEmpty = 0
linecounter=0
prevLine = ""

for line in f:
	if ">" in line:
		if countScaffolds != 0:
			lstLineLengths.append(currentBP)
			if currentBP == 0:
				numEmpty+=1
			fout.write(prevLine[:-1] + " " + str(currentBP) + "\n")
		countScaffolds+=1
		currentBP=0
		prevLine = line
	else:
		for item in line:
			if item == "A" or item == "T" or item == "C" or item =="G" or item == "N" or item == "a" or item == "t" or item == "g" or item == "c":
				currentBP+=1
	linecounter+=1
	if linecounter % 1000000 == 0:
		print(linecounter)

lstLineLengths.append(currentBP)

print(countScaffolds)
print(sum(lstLineLengths))
print(numEmpty)
fout.close()
f.close()
