inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged.fa"
outputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged_LargerThan-100000_BeginEnd10000.fasta"
length = 10000
thresholdLength = 100000


f = open(inputFile, 'r')
fout = open(outputFile, 'w')

currentContig = ""
counter =0
for line in f:
	if ">" in line:
		currentContig = line[:-1]
	else:
		if (len(line)-1) >=  thresholdLength:
			begin = line[:length]
			end = line[(len(line)-length-1):-1]
			fout.write(currentContig + "_First_" + str(length) +"\n")
			fout.write(begin + "\n")
			fout.write(currentContig + "_End_" + str(length) +"\n")
			fout.write(end + "\n")



			if counter % 100 == 0:
				print(counter)
			counter+=1

fout.close()
f.close()
