#Rewrite fasta files with list of contigs to remove

import sys

#inputFile = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/seqs/P_fer_HeterozygousParameters.contigs.purged.fa"
#outputFile = "P_fer_HeterozygousParameters.contigs.purged_RepurgedMMSplit_4_2_2024.fasta_retest"
#listAutomatedRemove = "ListOfRegionsToRemove_PurgeMultiMap_3_21_2024_Split.txt"
#listManualRemove = "ManualContigsToRemove.txt"

inputFile = sys.argv[1]
#print(inputFile)
outputFile = sys.argv[2]
#print(outputFile)
listAutomatedRemove = sys.argv[3]


dictDelete = {}
dictDeleteLeft = {}
dictDeleteRight = {}
dictDeleteBoth = {}


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


#print(len(dictDelete))
#print(len(dictDeleteLeft))
#print(len(dictDeleteRight))
#print(len(dictDeleteBoth))


fout = open(outputFile, 'w')
f = open(inputFile, 'r')

deleteWhole = 0
deleteRight = 0
deleteLeft = 0
deleteBoth = 0
deleteNone = 0

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

		#print("dboth", header)
	#if more than one take all starts and stops and choose the ones which will delete the most. Put that start and stop in the dictDeleteBoth dictionary
	if countOccurance > 1:
			#print(countOccurance)
			#print(header)
			counter+=1

			#lstStart = []
			#lstStop = []

			#lstRemove = [0,0,0,0]

			#if header in dictDeleteLeft:
				#print("delete left")
				#print(dictDeleteLeft[header])
				#temp = dictDeleteLeft[header]
				#lstRemove[0] = temp[0]
				#lstRemove[1] = temp[1]

			#if header in dictDeleteRight:
				#print("delete right")
				#print(dictDeleteRight[header])
				#temp = dictDeleteRight[header]
				#lstRemove = temp[2]
				#lstRemove = temp[3]

			#if header in dictDeleteBoth:
				#print("delete both")
				#print(dictDeleteBoth[header])
				#temp = dictDeleteBoth[header]
				#if temp[0] < lstRemove[0]:
				#	lstRemove[0] = temp[0]
				#if temp[1] > lstRemove[1]:
				#	lstRemove[1] = temp[1]

				#if temp[2] < lstRemove[2]:
				#	lstRemove[2] = temp[2]
				#if temp[3] > lstRemove[3]:
				#	lstRemove[3] = temp[3]

			dictDelete[header] = 1


	if header in dictDelete:
		deleteWhole+=1
		continue
	elif header in dictDeleteLeft:
		#write right
		deleteLeft+=1
		fout.write(">" + header +"_2 \n")
		coords = dictDeleteLeft[header]
		fout.write(sequence[coords[0]:coords[1]] + " \n")

	elif header in dictDeleteRight:
		#write left
		deleteRight+=1
		fout.write(">" + header +"_1 \n")
		coords = dictDeleteRight[header]
		fout.write(sequence[coords[0]:coords[1]] + " \n")

	elif header in dictDeleteBoth:
		#write right
		deleteBoth+=1
		fout.write(">" + header +"_2 \n")
		coords = dictDeleteBoth[header]
		fout.write(sequence[coords[2]:coords[3]] + " \n")

		#write left
		fout.write(">" + header +"_1 \n")
		fout.write(sequence[coords[0]:coords[1]] + " \n")

	else:
		deleteNone+=1
		fout.write(">" + header + " \n")
		fout.write(sequence + " \n")
	#counter+=1
	#if counter == 100:
	#	break


fout.close()
#print(counter)

print("Delete Whole Contig:", deleteWhole)
print("Delete Left Side of Contig:", deleteLeft)
print("Delete Right Side of Contig:", deleteRight)
print("Delete Both Sides of Contig:", deleteBoth)
print("Delete Nothing on Contig:", deleteNone)
