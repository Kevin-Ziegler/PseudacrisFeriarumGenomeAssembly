
#outputConfigFile = "/pool/KevinChorusFrogGenomeAssembly/OutputRepAHR/reads_file_1"

fileNames = "/KevinExternalDriveChorusFrogGenomeAssembly/ModifiedPE250/lstPEFiles.txt"
outputConfigFile = "/KevinExternalDriveChorusFrogGenomeAssembly/RepDenovoOutput/input_paired_end_reads.txt"
#fileNames = "/pool/PacBioAssembly/PE250/ListAllPEFastaFiles.txt"

f = open(fileNames, 'r')
fout = open(outputConfigFile, 'w')

lstFiles = []

for line in f:
	lstFiles.append(line)

f.close()


usedF = []

#/pool/PacBioAssembly/PE250/2015.08.07_L2/lane2_NoIndex_L002_R1_032.fasta
counter = 1

for i in range(0, len(lstFiles)):
	if lstFiles[i] in usedF:
		continue
	
	lastchar = ""	
	r12 = ""
	index = ""
	for j in range(0, len(lstFiles[i])):
		if lastchar + lstFiles[i][j] == "_R":
			r12 = lstFiles[i][j+1]
			index = j+1
		lastchar = lstFiles[i][j]

	#get other file	
	otherFile = ""
	print("Index: " + str(index))
	if r12 == "1":
		otherFile = lstFiles[i][:index] + "2" + lstFiles[i][index+1:]

	else:
		otherFile = lstFiles[i][:index] + "1" + lstFiles[i][index+1:]

	print(lstFiles[i])
	print(otherFile)

	index2 = ""
	for j in range(0, len(lstFiles)):
		if otherFile == lstFiles[j]:
			index2 = j

	usedF.append(lstFiles[i])
	usedF.append(lstFiles[index2])

			
	if r12 == "1":
		#fout.write(str(counter) + " " + lstFiles[i])
		#fout.write(str(counter) + " " + lstFiles[index2])
		fout.write(lstFiles[i][:-1] + " " + str(counter) + " 400 50 \n")
		fout.write(lstFiles[index2][:-1]+ " " + str(counter) + " 400 50 \n")
	if r12 == "2":
                #fout.write(str(counter) + " " + lstFiles[index2])
                #fout.write(str(counter) + " " + lstFiles[i])
		fout.write(lstFiles[index2][:-1] + " " + str(counter)+ " 400 50 \n")
		fout.write(lstFiles[i][:-1] + " " + str(counter)+ " 400 50 \n")
	counter+=1

fout.close()
	
	


	
