#idea of this program is to get coverage levels at every base pair towards the end of the contigs to be able to tell what they are? Repeats or not? Multiconnection or not
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
minLength = 100000

f = open(fileofContigs, 'r')
lengthofWindow = 10000
fout = open("CoverageOf_Beg_End_Contigs_10000.txt", 'w')



currentContigName = ""
counter=0
for line in f:
	if ">" in line:
		currentContigName = line[1:]
	else:
		if(len(line) < (2*(kmerLength + lengthofWindow))):
			continue
		if len(line) < minLength:
			continue
		begin = line[:lengthofWindow+kmerLength]
		temp = len(line)
		end = line[temp-lengthofWindow-kmerLength:-1]
		#print(begin)
		#print(end)

		#beginCov = np.zeros(lengthofWindow)
		#endCov = np.zeros(lengthofWindow)
		beginCov = [None] *lengthofWindow
		endCov = [None] * lengthofWindow


		for i in range(0, lengthofWindow):
			if i % 100 == 0:
				print(i)
			tempKmer = begin[i:i+kmerLength]
			#command = "jellyfish query " + jellyfishfile + " " + tempKmer
			output = runJellyQuery(jellyfishfile, tempKmer)
			split_out = output.stdout.split()
			#print(split_out)
			#a = "AT 01"
			#split_out = a.split() 
			beginCov[i] = float(split_out[1])

			tempKmer = end[i:i+kmerLength]
			#command = "jellyfish query " + jellyfishfile + " " + tempKmer
			output = runJellyQuery(jellyfishfile, tempKmer)
			split_out = output.stdout.split()
			#print(split_out)
			#a = "AT 01"
			#split_out = a.split()
			endCov[i] = float(split_out[1])



		#print(beginCov)
		#print(endCov)
		#if counter %2 == 0:
		print(counter)
		counter+=1

		fout.write(currentContigName)
		for i in range(0, lengthofWindow):
			fout.write(str(beginCov[i]) + " ")
		fout.write("\n")
		for i in range(0, lengthofWindow):
			fout.write(str(endCov[i]) + " ")
		fout.write("\n")
		fout.flush()

f.close()
fout.close()
