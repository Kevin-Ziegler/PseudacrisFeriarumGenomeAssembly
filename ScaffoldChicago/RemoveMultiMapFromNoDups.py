#The purpose of this file is to take a mergenodups file output by juicer's juicer2/juicer/CPU/common/sam_to_mnd.sh and remove multimapping reads using a dictionary object output from DoubleMappedReadsDictionary.py
#The output is a new merge no dups without multimapping reads

import pickle
import sys


#inputDups = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/aligned/merged_nodups.txt"
#inputMMDictionary = "MultiMappedReads_3_22_2024.pickle"
#outputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/aligned/merged_nodups_PurgedMM.txt"

#inputDups = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/OldMergeNoDups.txt"
#inputMMDictionary = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/MultiMappedReadsChicago.pickle"
#outputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/CHI_merged_nodups_PurgedMM.txt"

#inputDups = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds/old_mnd.txt"
#inputMMDictionary = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/MultiMappedReadsHIC_4_4_2024.pickle"
#outputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds/old_mnd_PurgedMM.txt"

#inputDups = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds_Try2_4_10_2024/aligned/nohup.out"
#inputMMDictionary = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/MultiMappedReadsHIC_4_10_2024.pickle"
#outputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/HiCMyChicagoScaffolds_Try2_4_10_2024/aligned/mnd_PurgeMM.txt"

inputDups = sys.argv[1]
inputMMDictionary = sys.argv[2]
outputFile = sys.argv[3]



dictMM = {}

with open(inputMMDictionary, "rb") as file:
	dictMM = pickle.load(file)

#print("read")
f = open(inputDups, 'r')

fout = open(outputFile, 'w')

counter = 0
for line in f:
	sline = line.split()
	if len(sline) > 1:
		read1 = sline[14]
		read2 = sline[15]
		if read1 in dictMM:
			continue
		elif read2 in dictMM:
			continue
		else:
			fout.write(line)

	counter+=1
	if counter % 1000000 == 0:
		#print(counter)
		fout.flush()


f.close()
fout.close()


