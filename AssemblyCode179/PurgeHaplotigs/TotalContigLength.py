inputFile = "MapIlluminaToCanu/clip.fasta"

f = open(inputFile, 'r')

lineNum = 0
countHeader = 0
totalLength = 0
numRepeats = 0
repeatLength = 0


for line in f:
	if ">" in line:
		sline = line.split()
		length = sline[1]
		length = length[4:]
		totalLength = totalLength + int(length)

		if sline[4] ==  "suggestRepeat=yes":
			numRepeats = numRepeats + 1
			totalLength = totalLength - int(length)
			repeatLength = repeatLength + int(length)

		countHeader+=1

	lineNum+=1

f.close()
print("Num Contigs:" + str(countHeader))
print("Total Length Non Repeats : " + str(totalLength))
print("Num Repeat Contigs: " + str(numRepeats))
print("Total Length Repeats : " + str(repeatLength))
