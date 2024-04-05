inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/clip.fasta"
outputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/clip_Colon.fasta"

f = open(inputFile , 'r')
fout = open(outputFile, 'w')


for line in f:
	if ":" in line:
		index = 0
		for i in range(0, len(line)):
			if line[i] == ":":
				index = i
		newline = ""
		for i in range(0, len(line)):
			if i == index:
				newline = newline + "_"
			else:
				newline = newline + line[i]
		fout.write(newline)
	else:
		fout.write(line)

f.close()
fout.close()
