inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/Try1_2_27_2024/P_fer_HeterozygousParameters.contigs.purged.0.assembly"


f = open(inputFile, 'r')


dictNumToContig = {}
dictNumToLength = {}

sum = 0

for line in f:
	if len(line) <= 1:
		continue
	if line[0] == ">":
		sline = line.split()
		num = sline[1]
		Length = int(sline[2])
		contig = sline[0][1:]
		#print(num, contig, Length)
		#break
		dictNumToContig[num] = contig
		dictNumToLength[num] = Length

	else:
		#print(line)
		sline = line.split()
		for item in sline:
			if item[0] == "-":
				item = item[1:]
			sum = sum + dictNumToLength[item]

print(sum)

f.close()
