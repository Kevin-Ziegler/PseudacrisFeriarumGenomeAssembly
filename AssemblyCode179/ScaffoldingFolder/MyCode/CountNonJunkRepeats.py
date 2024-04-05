inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/NonJunkRepeats"

f = open(inputFile, 'r')


lstNonJunkRepeats = []

for line in f:
	sline = line.split()
	if len(sline) > 0:
		temp = sline[1][4:]
		lstNonJunkRepeats.append(int(temp))

sumR = sum(lstNonJunkRepeats)


print("Total Length: " + str(sumR))
print("Number: " + str(len(lstNonJunkRepeats)))
print("Average: " + str(sumR/len(lstNonJunkRepeats)))

