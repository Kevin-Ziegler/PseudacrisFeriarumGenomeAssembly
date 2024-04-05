inputFile = "P_fer_HeterozygousParameters.contigs.purged.fa"
outputFile = "PurgedContigLengths.txt"

f = open(inputFile, 'r')
fout = open(outputFile, 'w')

for line in f:
	if ">" in line:
		fout.write(line[:-1] + " ")
	else:
		fout.write(str(len(line)-1) + " \n")

fout.close()
f.close()
