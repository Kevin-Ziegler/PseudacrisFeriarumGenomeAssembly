


def extractQueryFromBlast(fileName, query):
	f = open(fileName, 'r')

	flag_in_query = 0
	qlength = 0
	extractionName = []
	extractionSequence = []
	tempAlign = ""
	first = 0
	#list in format of [[query start, query stop], [subject start, subject stop], identity]
	subjectLengths = []
	numberResultsToTake = 1
	resultNumber = 0


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

				if sline[0] == "Identities":
					identity = sline[3][1:]
					identity = int(identity[:-3])
				if sline[0] == "Score" and len(sline) > 2:
					score = float(sline[2])


				if sline[0][0] == ">":


					if first != 0:
						extractionSequence.append(tempAlign)
					tempAlign = ["-"]*qlength
					first=1

					if resultNumber >= numberResultsToTake:
                                                break

					extractionName.append(sline[0][1:])
					resultNumber+=1

			if sline[0] == "Query":


				if identity < 70:
					continue

				start = int(sline[1])
				stop = int(sline[3])

				#check if unique sequence



				f.readline()
				line = f.readline()
				sline = line.split()
				seq = sline[2]
				subjectStart = int(sline[1])
				subjectStop = int(sline[3])
				#tempAlign[start-1:stop-1] = seq
				counter = 0

				flagAdd = 1
				replaceIndex = 0
				overlap = 0

				#if the marker is 75% unique or if the identity % is higher add it.
				for z in range(0, len(subjectLengths)):
					entry = subjectLengths[z]
					qstart = entry[0][0]
					qstop = entry[0][1]
					qidentity = entry[2]
					qscore = entry[3]

					print(start, stop)
					print(qstart, qstop)
					#on  right, could add according to this block
					if start > qstart and start > qstop:
						continue

					#on left, could add according to this block
					if stop < qstart:
						continue

					#overlap right
					if stop > qstop:
						totalDist = stop-start
						percentUnique = (totalDist - (qstop-start))/totalDist
						if percentUnique <= 0.25:
							#subjectLengths.append([[start,stop], [subjectStart, subjectStop], identity])
							flagAdd = 0
						overlap = 1

					#overlap left
					if start < qstart:
						totalDist = stop-start
						percentUnique = (totalDist - (qstart-stop))/totalDist
						if percentUnique <= 0.25:
							#subjectLengths.append([[start,stop], [subjectStart, subjectStop], identity])
							flagAdd = 0
						overlap = 1
					#Middle
					if start >= qstart and stop <= qstop:
						print("Middle")
						print(start, stop)
						print(qstart, qstop)
						percentUnique = ((qstop-qstart) - (start-stop))/(qstop-qstart)
						if percentUnique <= 0.25 or score < qscore:
							flagAdd = 0
						else:
							replaceIndex = z

				if flagAdd == 1:

					if replaceIndex == 0:
						subjectLengths.append([[start,stop], [subjectStart, subjectStop], identity, score])
						counter = 0
						for i in range(start-1, stop-1):
							tempAlign[i] = seq[counter]
							counter+=1

					else:
						clearstart = subjectLengths[replaceIndex][0][0]
						clearstop = subjectLengths[replaceIndex][0][1]

						for i in range(clearstart-1, clearstop-1):
							tempAlign[i] = "-"

						subjectLengths[replaceIndex] = [[start,stop], [subjectStart, subjectStop], identity, score]
						counter = 0
						for i in range(start-1, stop-1):
							tempAlign[i] = seq[counter]
							counter+=1

	


					
			if sline[0] == "Effective":
				extractionSequence.append(tempAlign)
				break

	return [extractionName, extractionSequence, subjectLengths]


#fileNameTranscripts = "NCBI_XenTrop_Gaba-a_transcripts.fasta"
#outdirc = "/home/alanlemmonlab/NeuronProject/Results/TestGaba_NCBI/"
#lstBlastResults = ["results.txt", "resultsXenTrop.txt", "resultsHourGlass.txt"]
#lstNames = ["Pfer_Transcript", "Pfer_Genome", "HourGlass_Genome", "XenTrop_Genome", "Mouse_Genome"]
#dircBlastResults = "/home/alanlemmonlab/NeuronProject/Data/BlastResults/XenTropGaba-A_NCBI_transcripts/"

fileNameTranscripts = "/home/alanlemmonlab/NeuronProject/Data/QuerySequences/Gaba-A_Subunits_NCBI_Orthologs/CombinedGabaXenTrop.fasta"
outdirc = "/home/alanlemmonlab/NeuronProject/Results/TestGaba_NCBI_Orthologs/"
#lstBlastResults = ["results.txt", "resultsXenTrop.txt", "resultsHourGlass.txt"]
lstNames = ["Pfer_Transcript_AminoAcid", "Pfer_Genome_AminoAcid"]
dircBlastResults = "/home/alanlemmonlab/NeuronProject/Data/BlastResults/XenTropGaba-A_NCBI_transcripts_AminoAcid_2/"
newFileNames = ["GABARA_alpha_1","GABARA_alpha_2", "GABARA_alpha_3", "GABARA_alpha_4", "GABARA_alpha_5", "GABARA_alpha_6"]

f = open(fileNameTranscripts, 'r')

lstTranscripts = []
lstRefSeq = []

lstGenes = []

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
	#outfile = open(outdirc + lstTranscripts[i] + ".fasta", 'w')
	outfile = open(outdirc + newFileNames[i] + ".fasta", 'w')
	outfile.write(">XenTrop_Transcript" + lstTranscripts[i] + " \n")
	outfile.write(lstRefSeq[i] + " \n")

	for j in range(0, len(lstNames)):
		blastFile = dircBlastResults + lstNames[j] + ".txt"
		print(lstTranscripts[i])
		temp = lstTranscripts[i].split()
		queryterm = temp[0]
		ans = extractQueryFromBlast(blastFile, queryterm)
		print(ans)
		if j == 1:
			lstGenes.append([ans[0], ans[2]])
		for k in range(0, len(ans[0])):
			outfile.write(">" + lstNames[j] + "_" + ans[0][k] + " \n")
			temp = ""
			for item in ans[1][k]:
				temp = temp + item
			outfile.write(temp + " \n")



	outfile.close()

print(lstGenes)
