inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/Pfer_Trimmed_Sorted.bed"
outputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/Pfer_Trimmed_Sorted_Colon.bed"

#inputFile = "t1"
#outputFile = "t2"

f = open(inputFile, 'r')
fout = open(outputFile , 'w')


lineCounter = 0

for line in f:

	sline = line.split()

	if len(sline) > 0 and ":" in sline[0]:
		index = 0
		for i in range(0, len(sline[0])):

			if sline[0][i] == ":":
				index = i
				break
		newline = ""
		for i in range(0, len(line)): 
			if i == index:
				newline = newline + "_"
			else:
				newline = newline + line[i]
		fout.write(newline)

	else:
		fout.write(line)
fout.close()
f.close()

