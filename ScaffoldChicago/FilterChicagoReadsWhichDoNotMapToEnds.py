#This file filters out reads > 40k from the ends of contigs. No much "real" Chicago interaction happens past this range. Inputs required are a nodups file and file of contig lengths.
#The outputs are new nodups file

import sys

#threshold = 40000
#contigLengthsFile = "RepurgedContigLengths_3_29_2024.txt"
#nodupsFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/CHI_merged_nodups_PurgedMM_RemoveSelf.txt"
#newNoDups = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/CHI_merged_nodups_PurgedMM_RemoveSelf_Trimm40kb.txt"

threshold = int(sys.argv[1])
contigLengthsFile = sys.argv[2]
nodupsFile = sys.argv[3]
newNoDups = sys.argv[4]

contigLengths = {}

f = open(contigLengthsFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 1:
		continue
	length = sline[4]
	contig = sline[2]
	contigLengths[contig] = int(length)

f.close()

f = open(nodupsFile, 'r')
fout = open(newNoDups, 'w')

counter = 0

for line in f:
	sline = line.split()
	if len(sline) > 1:
		contig1 = sline[1]
		loc1 = int(sline[2])

		contig2 = sline[5]
		loc2 = int(sline[6])

		length1 = 9999999
		length2 = 9999999
		if contig1 in contigLengths:
			length1 = contigLengths[contig1]
		if contig2 in contigLengths:
			length2 = contigLengths[contig2]
		thresholdlen1 = length1 - threshold
		thresholdlen2 = length2 - threshold

		#print(loc1)
		#print(thresholdlen1)



		if loc1 <= threshold or loc1 >= thresholdlen1:
			pass
		else:
			continue

		if loc2 <= threshold or loc2 >= thresholdlen2:
			pass
		else:
			continue

		fout.write(line)
		#print(line)
	if counter % 1000000 == 0:
		#print(counter)
		fout.flush()
	counter+=1


f.close()
fout.close()

