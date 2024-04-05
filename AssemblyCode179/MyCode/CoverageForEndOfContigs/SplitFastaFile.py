inputFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeDups/PipeLineOutput_PB/ChorusFrog.contigs/seqs/ChorusFrog.contigs.purged.fa"
numSubfiles = 50
subfileNames = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/temp"

f = open(inputFile, 'r')


#counter = 0
#for line in f:
#	counter+=1
#
#f.close()


listFiles = []
for i in range(0, numSubfiles):
	x = open(subfileNames + "_" + str(i) + ".fasta", 'w')
	listFiles.append(x)

f = open(inputFile, 'r')


counter = 0
counter2 = 0
for line in f:

	listFiles[counter2].write(line)
	#listFiles[counter2].write(line)
	if counter %2 ==1:
		counter2+=1
	counter2 = counter2%numSubfiles
	counter+=1

	if counter % 100 == 0:
		print(counter)

f.close()



for i in range(0, numSubfiles):
	listFiles[i].close()
