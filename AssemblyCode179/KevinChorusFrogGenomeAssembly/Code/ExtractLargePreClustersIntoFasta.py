inputFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/TestDifferentSCKmerThresholds/FullRun/ClusterRun1.txt"
outputFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/TestDifferentSCKmerThresholds/FullRun/ClusterRun1_Over25.txt"

f = open(inputFile, 'r')
f2 = open(outputFile, 'w')


for line in f:
	line = f.readline()
	sline = line.split()

	if len(sline) > 25:
		f2.write("T " + line)

f2.close()
f.close()
	
