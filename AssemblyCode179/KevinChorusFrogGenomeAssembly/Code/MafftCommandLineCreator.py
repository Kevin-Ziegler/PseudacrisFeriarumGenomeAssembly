#mafft --adjustdirection  Geneious_RC7.fasta > output_Geneious_RC7

import sys

inputStem = sys.argv[1]
outputStem = sys.argv[2]
numKmers = int(sys.argv[3])
outputCommandLineFile = sys.argv[4]

f = open(outputCommandLineFile, 'w')

for i in range(0, numKmers):
	f.write("mafft --adjustdirection  " + inputStem + str(i) + ".fasta" + " > " + outputStem + str(i) + ".fasta \n")
f.close()




