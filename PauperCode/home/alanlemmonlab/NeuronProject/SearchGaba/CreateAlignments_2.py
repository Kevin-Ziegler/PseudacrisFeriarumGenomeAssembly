


def extractQueryFromBlast(fileName, query):
	f = open(fileName, 'r')

	flag_in_query = 0
	qlength = 0
	extractionName = []
	extractionSequence = []
	tempAlign = ""
	first = 0

	for line in f:
		sline = line.split()
		if len(sline) < 1:
			continue

		if sline[0] == "Query=":
			#print(sline[1])
			#print(query)
			if sline[1] == query:
				flag_in_query = 1
				while(1==1):
					temp = f.readline()
					if len(temp) > 7:
						if temp[:7] == "Length=":
							qlength = int(temp[7:])
							break
				continue

		if flag_in_query == 1:
			if len(sline[0]) > 1:
				if sline[0][0] == ">":
					extractionName.append(sline[0][1:])
					if first != 0:
						extractionSequence.append(tempAlign)
					tempAlign = ["-"]*qlength
					first=1

			if sline[0] == "Query":
				start = int(sline[1])
				stop = int(sline[3])
				f.readline()
				line = f.readline()
				sline = line.split()
				seq = sline[2]
				#tempAlign[start-1:stop-1] = seq
				counter = 0
				for i in range(start-1, stop-1):
					tempAlign[i] = seq[counter]
					counter+=1

			if sline[0] == "Effective":
				extractionSequence.append(tempAlign)
				break

	return [extractionName, extractionSequence]


#fileNameTranscripts = "NCBI_XenTrop_Gaba-a_transcripts.fasta"
#outdirc = "/home/alanlemmonlab/NeuronProject/Results/TestGaba_NCBI/"
#lstBlastResults = ["results.txt", "resultsXenTrop.txt", "resultsHourGlass.txt"]
#lstNames = ["Pfer_Transcript", "Pfer_Genome", "HourGlass_Genome", "XenTrop_Genome", "Mouse_Genome"]
#dircBlastResults = "/home/alanlemmonlab/NeuronProject/Data/BlastResults/XenTropGaba-A_NCBI_transcripts/"

fileNameTranscripts = "/home/alanlemmonlab/NeuronProject/Data/QuerySequences/Gaba-A_Subunits_NCBI_Orthologs/CombinedGabaXenTrop.fasta"
outdirc = "/home/alanlemmonlab/NeuronProject/Results/TestGaba_NCBI_Orthologs/"
#lstBlastResults = ["results.txt", "resultsXenTrop.txt", "resultsHourGlass.txt"]
lstNames = ["Pfer_Transcript", "Pfer_Genome"]
dircBlastResults = "/home/alanlemmonlab/NeuronProject/Data/BlastResults/XenTropGaba-A_NCBI_transcripts_AminoAcid_2/"


f = open(fileNameTranscripts, 'r')

lstTranscripts = []
lstRefSeq = []

temp = ""

flag = 0

for line in f:
	if len(line) > 1:
		if line[0] == ">":
			if flag == 1:
				lstRefSeq.append(temp)

			lstTranscripts.append(line[1:-1])
			flag = 1
			temp = ""
		else:
			temp = temp + line[:-1]

lstRefSeq.append(temp)
print(lstTranscripts)


for i in range(0, len(lstTranscripts)):
	outfile = open(outdirc + lstTranscripts[i] + ".fasta", 'w')
	outfile.write(">XenTrop_Transcript" + lstTranscripts[i] + " \n")
	outfile.write(lstRefSeq[i] + " \n")

	for j in range(0, len(lstNames)):
		blastFile = dircBlastResults + lstNames[j] + ".txt"
		print(lstTranscripts[i])
		temp = lstTranscripts[i].split()
		queryterm = temp[0]
		ans = extractQueryFromBlast(blastFile, queryterm)
		#print(ans)
		for k in range(0, len(ans[0])):
			outfile.write(">" + lstNames[j] + "_" + ans[0][k] + " \n")
			temp = ""
			for item in ans[1][k]:
				temp = temp + item
			outfile.write(temp + " \n")



	outfile.close()
