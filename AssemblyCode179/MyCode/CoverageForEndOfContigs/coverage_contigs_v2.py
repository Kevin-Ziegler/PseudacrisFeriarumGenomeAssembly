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
#outputFile = sys.argv[2]

#fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.fasta"
fileofContigs = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged.fa"
outputFile = "Contig_v2_Coverage2.txt"

jellyfishfile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/KevinChorusFrogGenomeAssembly/reads_All_21.jf"
kmerLength = 21
minLength = 50000
parallel = 100

f = open(fileofContigs, 'r')
lengthofWindow = 10000
fout = open(outputFile, 'w')



currentContigName = ""
counter=0
seq = ""
currentContigName = ""
newContig = ""

for line in f:
	if ">" in line:
		currentContigName = newContig
		newContig = line[1:]

		if(len(seq) < (2*(kmerLength + lengthofWindow))):
			seq = ""
			continue
		if len(seq) < minLength:
			seq = ""
			continue
		begin = seq[:lengthofWindow+kmerLength]
		temp = len(seq)
		end = seq[temp-lengthofWindow-kmerLength:-1]
		#print(begin)
		#print(end)

		#beginCov = np.zeros(lengthofWindow)
		#endCov = np.zeros(lengthofWindow)
		beginCov = [None] *lengthofWindow
		endCov = [None] * lengthofWindow


		tempForwardKmers = ""
		tempBackwardKmers = ""
		index = 0

		for i in range(0, lengthofWindow+1):
			if i % parallel == 0 and tempForwardKmers != "":
				#print(i)
				command = "jellyfish query " + jellyfishfile + " " + tempForwardKmers
				command = command.split()
				output = runJellyQuery(jellyfishfile, command)
				split_out = output.stdout.split()
				#print(split_out)

				command = "jellyfish query " + jellyfishfile + " " + tempBackwardKmers
				command = command.split()
				output = runJellyQuery(jellyfishfile, command)
				split_outB = output.stdout.split()
				#print(split_outB)


				for j in range(0, len(split_out)):
					if j %2 == 0:
						continue
					else:
						beginCov[index] = float(split_out[j])
						endCov[index] = float(split_outB[j])
						index+=1

				tempForwardKmers = ""
				tempBackwardKmers = ""


			if i == lengthofWindow:
				break


			tempKmer = begin[i:i+kmerLength]
			#command = "jellyfish query " + jellyfishfile + " " + tempKmer
			#output = runJellyQuery(jellyfishfile, tempKmer)
			#split_out = output.stdout.split()
			#print(split_out)
			#a = "AT 01"
			#split_out = a.split() 
			#beginCov[i] = float(split_out[1])

			tempForwardKmers = tempForwardKmers + tempKmer + " "

			tempKmer = end[i:i+kmerLength]
			#command = "jellyfish query " + jellyfishfile + " " + tempKmer
			#output = runJellyQuery(jellyfishfile, tempKmer)
			#split_out = output.stdout.split()
			#print(split_out)
			#a = "AT 01"
			#split_out = a.split()
			#endCov[i] = float(split_out[1])
			tempBackwardKmers = tempBackwardKmers + tempKmer + " "


		#print(beginCov)
		#print(endCov)
		#if counter %2 == 0:
		print(counter)
		counter+=1

		if counter% 1000 == 0:
			print(counter)

		fout.write(currentContigName)
		for i in range(0, lengthofWindow):
			fout.write(str(beginCov[i]) + " ")
		fout.write("\n")
		for i in range(0, lengthofWindow):
			fout.write(str(endCov[i]) + " ")
		fout.write("\n")
		fout.flush()

		#currentContigName = line[1:]
		seq = ""

	else:
		seq = seq + line[:-1]
		#print(seq)
f.close()
fout.close()
