inputFile = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/seqs/P_fer_HeterozygousParameters.contigs.purged.fa"
outputFile = "P_fer_HeterozygousParameters.contigs.purged_RepurgedMMSplit_4_2_2024.fasta"
listAutomatedRemove = "ListOfRegionsToRemove_PurgeMultiMap_3_21_2024_Split.txt"
listManualRemove = "ManualContigsToRemove.txt"

dictDelete = {}
dictDeleteLeft = {}
dictDeleteRight = {}
dictDeleteBoth = {}

"""
#Add manual remove contigs to the dictionary
f = open(listManualRemove, 'r')
for line in f:
	line = line[:-1]
	dictDelete[line] = 1

f.close()

"""

#Add Automated contigs to dictionaries
f = open(listAutomatedRemove, 'r')

for line in f:
	l2 = f.readline()
	l3 = f.readline()
	#loci+=1
	l3s = l3.split()
	if len(l3s) == 2:
		l2s = l2.split()
		totalL = int(l2s[1])
		#Remove completely
		if l3s[0] == "0" and int(l3s[1]) == totalL:
			dictDelete[l2s[0]] = 1
		#Delete Left
		elif l3s[0] == "0":
			dictDeleteLeft[l2s[0]] = [int(l3s[1]), totalL]
		#Delete Right
		elif int(l3s[1]) == totalL:
			dictDeleteRight[l2s[0]] = [0, int(l3s[0])]
		#Delete middle
		else:
			dictDeleteBoth[l2s[0]] = [0,int(l3s[0]), int(l3s[1]), totalL]
f.close()


print(len(dictDelete))
print(len(dictDeleteLeft))
print(len(dictDeleteRight))
print(len(dictDeleteBoth))


fout = open(outputFile, 'w')
f = open(inputFile, 'r')

counter = 0
for line in f:
	header = line[1:-1]
	sequence = f.readline()
	sequence = sequence[:-1]
	#print(header)

	countOccurance = 0

	if header in dictDeleteLeft:
		countOccurance+=1
	if header in dictDeleteRight:
		countOccurance+=1
	if header in dictDeleteBoth:
		countOccurance+=1
	if countOccurance > 1:
			print(countOccurance)
			print(header)
			counter+=1

			if header in dictDeleteLeft:
				print("delete left")
				print(dictDeleteLeft[header])
			if header in dictDeleteRight:
				print("delete right")
				print(dictDeleteRight[header])
			if header in dictDeleteBoth:
				print("delete both")
				print(dictDeleteBoth[header])


	if header in dictDelete:
		continue
	elif header in dictDeleteLeft:
		#write right
		fout.write(">" + header +"_2 \n")
		coords = dictDeleteLeft[header]
		fout.write(sequence[coords[0]:coords[1]] + " \n")

	elif header in dictDeleteRight:
		#write left
		fout.write(">" + header +"_1 \n")
		coords = dictDeleteRight[header]
		fout.write(sequence[coords[0]:coords[1]] + " \n")

	elif header in dictDeleteBoth:
		#write right
		fout.write(">" + header +"_2 \n")
		coords = dictDeleteBoth[header]
		fout.write(sequence[coords[2]:coords[3]] + " \n")

		#write left
		fout.write(">" + header +"_1 \n")
		fout.write(sequence[coords[0]:coords[1]] + " \n")

	else:
		fout.write(">" + header + " \n")
		fout.write(sequence + " \n")
	#counter+=1
	#if counter == 100:
	#	break


fout.close()
print(counter)
