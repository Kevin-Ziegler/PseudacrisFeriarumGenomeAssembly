#inputSCPosFile = "outputSC_RC_Pos.txt"
#inputSCPosFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/WholeGenomeHiC_Connections_July_31/outputSC_Full_Both.txt"
#inputSCPosFile = "SCKmers_POS_delta.txt"

import sys
import os

inputSCPosFile = sys.argv[1]
inputSCGeneiousFolder = sys.argv[2]

numLinesToEstimateFrom = 10000

f = open(inputSCPosFile, 'r')


numLines = 0
numSCLines = 0
numTotalSC = 0


for line in f:
	numLines+=1

	if line == "\n":
		pass
	else:
		numSCLines+=1
		sline = line.split("\t")
		numTotalSC = numTotalSC + len(sline)

	if numLines == numLinesToEstimateFrom:
		break

f.close()

files = os.listdir(inputSCGeneiousFolder)
lstNumPBReads = []

for i in range(0, len(files)):
	f = open(inputSCGeneiousFolder + files[i], 'r')
	
	numPB = 0
	for line in f:
		if ">" in line:
			numPB+=1
	numPB-=1
	lstNumPBReads.append(numPB)
	f.close()


avgPB = sum(lstNumPBReads)/len(lstNumPBReads)
lstAverageAlignmentLength = []


for i in range(0, len(files)):
	f = open(inputSCGeneiousFolder + files[i], 'r')

	numCharacters = 0
	counter = 0
	for line in f:
		if counter == 0:
			counter+=1
			continue
		if ">" in line:
			break		
		numCharacters = numCharacters + len(line)
		counter+=1
	
	lstAverageAlignmentLength.append(numCharacters)
	f.close()

avgAlignLength = sum(lstAverageAlignmentLength)/len(lstAverageAlignmentLength)

print("Stats: ")
print("Total Lines: " + str(numLines))
print("Number PB Reads with SC Kmer: " + str(numSCLines))
print("Total Number SC Kmers: " + str(numTotalSC))
print("AvgPB per SC Kmer: " + str(avgPB))
print("Avg Aligned SC Kmer: " + str(avgAlignLength))
