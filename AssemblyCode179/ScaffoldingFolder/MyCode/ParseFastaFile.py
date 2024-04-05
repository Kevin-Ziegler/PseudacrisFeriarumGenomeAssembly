#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedHIC/scaffolds_FINAL.fasta"
#outputFile = "stats_HIC.txt"
#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedChicago/scaffolds_FINAL.fasta"
#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/clip.fasta"

#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.fasta"
#outputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/stats_HIC_COUNT_N_v2.txt"

inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/Try2GATC/scaffolds_CHI_v2_GATC.fasta"
outputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/Try2GATC/stats_scaffolds_CHI_v2_GATC.fasta"



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
			fout.write(prevLine[1:-1] + "\t" + str(currentBP) + "\n")
		countScaffolds+=1
		currentBP=0
		prevLine = line
	else:
		for item in line:
			if item == "A" or item == "T" or item == "C" or item =="G" or item == "N":
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
