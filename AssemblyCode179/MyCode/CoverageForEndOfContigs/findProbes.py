#idea of this program is to get probs which are a series of things at a certain coverage level
import os
import subprocess
import numpy as np

def runJellyQuery(jf_file, kmer):
	temp = subprocess.run(["jellyfish", "query", jf_file, kmer], capture_output=True)
	return temp



#fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ChorusFrog_Canu_CLR_2/ChorusFrog.contigs.fasta"
fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeDups/PipeLineOutput_PB/ChorusFrog.contigs/seqs/ChorusFrog.contigs.purged.fa"
jellyfishfile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/KevinChorusFrogGenomeAssembly/reads_All_21.jf"
kmerLength = 21

f = open(fileofContigs, 'r')
probeLength = 120
percentSingleCov = 0.6
threshold_High = 120
threshold_Low = 80



fout = open("TestProbe.txt", 'w')


currentContigName = ""
counter = 0
counterPosition = 0
for line in f:
	if ">" in line:
		currentContigName = line[1:]
		fout.write(currentContigName)
		
	else:
		#forward probe
		#first probe length
		forwardProbe = [0,0]
		count_Satisfactory = 0 

		listCov = []
		#listTotal = []
		for i in range(0, probeLength):
			tempKmer = line[i:i+kmerLength]
			output = runJellyQuery(jellyfishfile, tempKmer)
			split_out = output.stdout.split()
			coverage = float(split_out[1])
			#listTotal.append(coverage)
			fout.write(str(coverage) + " " )
			if coverage < threshold_High and coverage > threshold_Low:
				count_Satisfactory+=1
				listCov.append(1)
			else:
				listCov.append(0)

		#check if first 120 make good probe

		if count_Satisfactory > (probeLength * percentSingleCov):
			forwardProbe[1] = probeLength-1
		else:
			position = 0
			counterPosition = 120
			for i in range(probeLength, len(line)):
				tempKmer = line[i:i+kmerLength]
				output = runJellyQuery(jellyfishfile, tempKmer)
				split_out = output.stdout.split()
				coverage = float(split_out[1])
				#listTotal.append(coverage)
				fout.write(str(coverage) + " ")
				covOfLeavingPosition = listCov[position]
				count_Satisfactory = count_Satisfactory - covOfLeavingPosition
				if coverage < threshold_High and coverage > threshold_Low:
					count_Satisfactory+=1
					listCov[position] = 1
				else:
					listCov[position] = 0
				position+=1
				counterPosition+=1
				position = position % probeLength
				#print(counterPosition)
				if count_Satisfactory > (probeLength * percentSingleCov):
					forwardProbe[0] = i-probeLength
					forwardProbe[1] = i
					break
		fout.write("\n")
		fout.write(str(forwardProbe[0]) + " " + str(forwardProbe[1]) + " \n")
		print(forwardProbe)
		#for i in range(0, len(listTotal)):
		#	fout.write(str(listTotal[i]) + " ")
		#fout.write("\n")
		fout.flush()

		print(counter)
		counter+=1

f.close()
fout.close()
