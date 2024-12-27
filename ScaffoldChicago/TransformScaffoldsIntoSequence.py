#The purpose of this file is to take the Juicer style .assembly file and the orginal contig fasta file to make a new fasta file conntaining the new chicago scaffolds

import sys

#scaffoldFile = "JuiceBoxMyChicagoScaffolds.assembly"
#sequencefile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/P_fer_HeterozygousParameters.contigs.purged_RepurgedMMSplit_NoSpace_3_23_2024.fasta"
#dictJuiceBoxNamesFile = "JuiceBoxChicagoNames.txt"
#scaffoldOutputFasta = "MyChicagoScaffolds_4_10_2024.fasta"
#scaffoldOutputFastaKey = "MyChicagoScaffoldsKey_4_10_2024.txt"


scaffoldFile = sys.argv[1]
sequencefile = sys.argv[2]
dictJuiceBoxNamesFile = sys.argv[3]
scaffoldOutputFasta = sys.argv[4]
scaffoldOutputFastaKey = sys.argv[5]


def createReverseComplement(sequence):
	rc = ""
	reverse = sequence[::-1]
	for item in reverse:
		if item == "A":
			rc = rc + "T"
		if item == "T":
			rc = rc + "A"
		if item == "G":
			rc = rc + "C"
		if item == "C":
			rc = rc + "G"
	return rc


names = {}
contigNames = []
f = open(dictJuiceBoxNamesFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 2:
		continue
	contig = sline[0][1:]
	name = sline[1]
	names[name] = contig
	contigNames.append(contig)
f.close()





ShouldFullyPurgeMissed = []



usedContigs = {}

for item in ShouldFullyPurgeMissed:
	usedContigs[item] = 1


sequences = {}
f = open(sequencefile, 'r')

for line in f:
	line = line.strip()
	contig = line[1:]
	line2 = f.readline()
	sequence = line2.strip()
	sequences[contig] = sequence
f.close()


f = open(scaffoldFile, 'r')


filler = "N" *500


fout = open(scaffoldOutputFasta, 'w')
fout2 = open(scaffoldOutputFastaKey, 'w')

scaffoldCounter = 1
for line in f:
	sline = line.split()
	if len(sline) <= 1:
		continue

	combinedSequence = ""

	scaffoldName = "Scaffold_" + str(scaffoldCounter)
	#print(scaffoldCounter)
	scaffoldCounter+=1
	key = ""

	for item in sline:
		if item[0] == "-":
			temp = item[1:]
			contig = names[temp]
			seq = sequences[contig]
			#flipped_seq = seq[::-1]
			flipped_seq = createReverseComplement(seq)
			usedContigs[contig] = 1
			combinedSequence = combinedSequence + flipped_seq + filler
			key = key + "-" + contig + " "
		else:
			contig = names[item]
			seq = sequences[contig]
			usedContigs[contig] = 1
			combinedSequence = combinedSequence + seq + filler
			key = key + contig + " "

	combinedSequence = combinedSequence[:-500]
	#print(scaffoldName + " \n")
	#print(combinedSequence + " \n")
	fout.write(">" + scaffoldName + "\n")
	fout.write(combinedSequence + "\n")
	fout2.write(">" + scaffoldName + "\n")
	fout2.write(key + "\n")
	if scaffoldCounter % 100 == 0:
		fout.flush()


f.close()

#print(len(contigNames))
#print(len(usedContigs))

for item in contigNames:
	if item in usedContigs:
		continue
	seq = sequences[item]
	fout.write(">Scaffold_" + str(scaffoldCounter) + "\n")
	fout.write(seq + "\n")
	fout2.write(">Scaffold_" + str(scaffoldCounter) + "\n")
	fout2.write(item + " \n")
	usedContigs[item] = 1
	scaffoldCounter+=1
	if scaffoldCounter % 1000 == 0:
		fout.flush()

fout.close()
fout2.close()
