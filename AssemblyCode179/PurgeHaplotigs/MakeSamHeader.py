inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Corrected_CLR_Reads/ChorusFrog.correctedReads.fasta"
outputFileName = "SamHeader_CorrectedCLR.txt"

inputFile = open(inputFileName, 'r')
outputFile = open(outputFileName, 'w')


#@SQ	SN:tig00000001	LN:1001576


counter = 0
length = 0
newHeader = ""

for line in inputFile:
	if line[0] != ">":
		continue
	else:
		sline = line.split()
		newHeader = "@SQ\tSN:" + sline[0][1:] + "\tLN:" + sline[1][4:] + " \n"
		outputFile.write(newHeader)

	counter+=1


outputFile.close()
inputFile.close()
