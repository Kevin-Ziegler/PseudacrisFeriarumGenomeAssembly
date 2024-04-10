inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/Pfer_Trimmed_Sorted.bed"

f = open(inputFile, 'r')

counter = 0
for line in f:
	sline = line.split()
	if ":" in sline[0]:
		print(line)
		counter+=1
		print(counter)

f.close()
