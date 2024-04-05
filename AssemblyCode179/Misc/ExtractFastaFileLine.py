import sys

#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/ChorusFrog.unitigs.fasta"

#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/scaffolds_FINAL.fasta"

#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/Combined_HIC_1.fasta"
inputFileName = sys.argv[1]

#outputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/EnzymeCheck_HiC.txt"
#outputFileName = "outputfile.txt"
outputFileName = sys.argv[2]

inputFile = open(inputFileName, 'r')
outputFile = open(outputFileName, 'w')

header = sys.argv[3]
#header = "@GWNJ-0957:266:GW1808031300:4:1101:10003:10029"
#header = "@GWNJ-0957:266:GW1808031300:4:1101:10003:10029"
#header = "@GWNJ-0957:266:GW1808031300:4:1101:7405:1204"

flagFound = 0
counter = 0
for line in inputFile:
	sline = line.split()
	if line[0] == ">" and flagFound == 1:
		break

	if header in sline[0]:
		flagFound = 1

	if flagFound == 1:
		outputFile.write(line)
	counter+=1
	if counter % 100000 == 0:
		print(counter)

inputFile.close()
outputFile.close()


