inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedChicago/scaffolds_FINAL.agp"
#inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedHIC/scaffolds_FINAL.agp"
#inputFile = "t1"

f = open(inputFile, 'r')

prevName = "scaffold_1"
currentLinks = 0

lstLinks =[]

for line in f:
	sline = line.split()
	if len(sline) > 1:

		if sline[0] == prevName:
			currentLinks+=1

		else:
			lstLinks.append(int(currentLinks-(currentLinks-1)/2))
			print(int(currentLinks-(currentLinks-1)/2))
			currentLinks = 1
		prevName = sline[0]

f.close()
print(lstLinks)
