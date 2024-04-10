#0 tig00008626_1 115130 335 16 tig00009951_1 17439 51 0 150M CTGGGACCTGGCAGGTGTGTCCGCGGTGTAGCTCCACTTGTGAAATCTTCGGGCCCGAACAGCCGGCGTGACCCCCAGGCGAGCCAGGATCTCAATTTTTAGTTTAGCATAGTCCCGGACATCCTGCTCCCTGAGGTCATAGTAGGCCTT 0 150M CGTCTGCCCATTCTTCCATCGGCAGTCTCTCCCTTTCCGCCACTCTCTCAAACACGCCGAGGTAGGCTTCTACATCGTCGTTAGGGGTCATTTTCTGCAGGGCCCGCTGTACAATCTTCCTGATACTAGTAGACTCCGCCGGGTTTATCA GWNJ-0957:266:GW1808031300:4:2220:5223:38456 GWNJ-0957:266:GW1808031300:4:2220:5223:38456 
import pickle

#Going to read in all connections and output a dictionary where input is contig1_contig2 = number of connections



#inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/aligned/merged_nodups_PurgedMM_RemoveSelf.txt"

inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/aligned/CHI_merged_nodups_PurgedMM_RemoveSelf_Trimm40kb.txt"

#inputFile = "dumbtest"
output = "CHI_purgedups_Trimmed_Connections.pickle"


dictConnections = {}

f = open(inputFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 1:
		continue

	contig1 = sline[1]
	contig2 = sline[5]

	#checkMapq
	mapq1 = sline[8]
	mapq2 = sline[11]

	if mapq1 == "0" and mapq2 == "0":
		continue


	both1 = contig1+"_"+contig2
	both2 = contig2+"_"+contig1
	if both1 in dictConnections:
		dictConnections[both1] = dictConnections[both1] + 1
	else:
		dictConnections[both1] = 1

	if both2 in dictConnections:
		dictConnections[both2] = dictConnections[both2] + 1
	else:
		dictConnections[both2] = 1


f.close()

with open(output, "wb") as file:
	pickle.dump(dictConnections, file)

