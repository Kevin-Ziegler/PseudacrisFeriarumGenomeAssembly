#0 tig00008626_1 115130 335 16 tig00009951_1 17439 51 0 150M CTGGGACCTGGCAGGTGTGTCCGCGGTGTAGCTCCACTTGTGAAATCTTCGGGCCCGAACAGCCGGCGTGACCCCCAGGCGAGCCAGGATCTCAATTTTTAGTTTAGCATAGTCCCGGACATCCTGCTCCCTGAGGTCATAGTAGGCCTT 0 150M CGTCTGCCCATTCTTCCATCGGCAGTCTCTCCCTTTCCGCCACTCTCTCAAACACGCCGAGGTAGGCTTCTACATCGTCGTTAGGGGTCATTTTCTGCAGGGCCCGCTGTACAATCTTCCTGATACTAGTAGACTCCGCCGGGTTTATCA GWNJ-0957:266:GW1808031300:4:2220:5223:38456 GWNJ-0957:266:GW1808031300:4:2220:5223:38456 
import pickle

#Record connections between contigs who have more than 10 connections


#inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/aligned/merged_nodups_PurgedMM_RemoveSelf.txt"

inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/CHI_merged_nodups_PurgedMM_RemoveSelf_Trimm40kb.txt"

#inputFile = "dumbtest"
output = "CHI_purgedups_Trimmed_Connections_Locations.pickle"

inputDictionaryConnections = "CHI_purgedups_Trimmed_Connections.pickle"

dictConnectionCounts = {}


# Read the dictionary back from the file
with open(inputDictionaryConnections, "rb") as file:
	dictConnectionCounts = pickle.load(file)
	#list2 = loaded_data


dictConnections = {}

f = open(inputFile, 'r')

counter = 0
for line in f:
	if counter %1000000 == 0:
		print(counter)
	counter+=1

	sline = line.split()
	if len(sline) < 1:
		continue

	contig1 = sline[1]
	contig2 = sline[5]

	location1 = int(sline[2])
	location2 = int(sline[6])

	#checkMapq
	mapq1 = sline[8]
	mapq2 = sline[11]

	if mapq1 == "0" and mapq2 == "0":
		continue


	both1 = contig1+"_"+contig2
	both2 = contig2+"_"+contig1

	if both1 in dictConnectionCounts:
		if dictConnectionCounts[both1] >= 8:
			pass
		else:
			continue
	coords1 = [location1, location2]
	coords2 = [location2, location1]

	if both1 in dictConnections:
		#print("In:")
		#print(dictConnections[both1])
		#print(both1)
		#temparray = dictConnections[both1]
		#temparray
		dictConnections[both1].append(coords1)
	else:
		dictConnections[both1] = [coords1]

	if both2 in dictConnections:
		dictConnections[both2].append(coords2)
	else:
		dictConnections[both2] = [coords2]


f.close()

with open(output, "wb") as file:
	pickle.dump(dictConnections, file)

