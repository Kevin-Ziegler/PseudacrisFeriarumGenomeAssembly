#idea of this program is to get coverage levels at every base pair towards the end of the contigs to be able to tell what they are? Repeats or not? Multiconnection or not
import os
import subprocess
import numpy as np
import sys

def runJellyQuery(jf_file, command):
	temp = subprocess.run(command, capture_output=True)
	return temp



#fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ChorusFrog_Canu_CLR_2/ChorusFrog.contigs.fasta"
#fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeDups/PipeLineOutput_PB/ChorusFrog.contigs/seqs/ChorusFrog.contigs.purged.fa"
#fileofContigs = sys.argv[1]
#fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.fasta"
fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged.fa"

outputFile = "RestrictionSites_GATC.txt"

jellyfishfile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/KevinChorusFrogGenomeAssembly/reads_All_21.jf"
kmerLength = 21
minLength = 50000
parallel = 100

restrictionEnzyme = "GATC"
restrictionEnzyme_rc = "GATC"
lenRestriEn = 4

f = open(fileofContigs, 'r')
lengthofWindow = 10000
fout = open(outputFile, 'w')



currentContigName = ""
counter=0
seq = ""
newContigName = ""

for line in f:
	if ">" in line:
		currentContigName = newContigName
		newContigName = line[1:]
		if(len(seq) < (2*(kmerLength + lengthofWindow))):
			seq = ""
			continue
		if len(seq) < minLength:
			seq = ""
			continue
		lstRestrictionSites_Begin = []
		lstRestrictionSites_End = []
		begin = seq[:lengthofWindow]
		temp = len(seq)
		end = seq[temp-lengthofWindow:-1]

		for i in range(0, len(begin)-lenRestriEn):
			if begin[i:i+lenRestriEn] == restrictionEnzyme or begin[i:i+lenRestriEn] == restrictionEnzyme_rc:
				lstRestrictionSites_Begin.append([i,i+lenRestriEn ])
			if end[i:i+lenRestriEn ] == restrictionEnzyme or end[i:i+lenRestriEn ] == restrictionEnzyme_rc:
				lstRestrictionSites_End.append([i,i+lenRestriEn ])



		#print(lstRestrictionSites_Begin)
		for i in range(0,len(lstRestrictionSites_Begin)):
			fout.write(str(lstRestrictionSites_Begin[i][0]) + " " + str(lstRestrictionSites_Begin[i][1]) + " ")
		fout.write("\n")

		for i in range(0,len(lstRestrictionSites_End)):
			fout.write(str(lstRestrictionSites_End[i][0]) + " " + str(lstRestrictionSites_End[i][1]) + " ")
		fout.write("\n")

		counter+=1
		if counter%1000 == 0:
			print(counter)
		seq = ""
	else:
		seq = seq + line[:-1]
f.close()
fout.close()
