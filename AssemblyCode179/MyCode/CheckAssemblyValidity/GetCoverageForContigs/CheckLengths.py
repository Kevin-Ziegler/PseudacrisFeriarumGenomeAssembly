hf = "ContigHeaders.txt"

f = open(hf, 'r')

lsth = []
for line in f:
	lsth.append(line[:-1])

f.close()


print(lsth)



fL = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/PurgedContigLengths.txt"

f = open(fL, 'r')

for line in f:
	if len(line) < 1:
		continue

	sline = line.split()
	header = sline[0][1:]
	if header in lsth:
		print(header)
		print(sline[1])


f.close()
