scaffoldOrderFile = "/home/alanlemmonlab/Scaffold_AidenLab/Try1_2_27_2024/P_fer_HeterozygousParameters.contigs.purged.0.assembly"
connectionsFile = "/home/alanlemmonlab/Scaffold_AidenLab/juicer-1.6/aligned/merged_nodups.txt"
outputFolder = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/XYCoords3/"


contigNumbers = {}
contigConnections = {}

fin = open(scaffoldOrderFile, 'r')

for line in fin:
	if len(line) < 1:
		continue

	sline = line.split()
	if line[0] == ">":
		contigNumbers[sline[1]] = sline[0][1:]

	elif len(sline) > 1:
		print(sline)
		for i in range(0, len(sline)):

			prevName = None
			nextName = None

			contigNumber = sline[i]
			if contigNumber[0] == "-":
				contigNumber = contigNumber[1:]
			if i != 0:
				prev = sline[i-1]
				if prev[0] == "-":
					prev = prev[1:]
				prevName = contigNumbers[prev]


			if i != (len(sline)-1):
				next = sline[i+1]
				if next[0] == "-":
					next = next[1:]
				nextName = contigNumbers[next]

			contigNumberName = contigNumbers[contigNumber]
			#prevName = contigNumbers[prev]
			#nextName = contigNumbers[next]
			contigConnections[contigNumberName] = [prevName, nextName]

print(contigConnections)



f = open(connectionsFile, 'r')

counter = 0
for line in f:
	if counter % 1000000 == 0:
		print(counter)
	sline = line.split()
	contig1 = sline[1]
	contig2 = sline[5]

	if contig1 in contigConnections:

		connections = contigConnections[contig1]
		if contig2 in connections:
			prev = None
			next = None
			prevCon = None
			nextCon = None

			if contig2 == connections[0]:
				prev = contig2
				prevCon = sline[6]
				next = contig1
				nextCon = sline[2]
			else:
				prev = contig1
				prevCon = sline[2]
				next = contig2
				nextCon = sline[6]

			fout = open(outputFolder + prev + "_" + next + "Connections.txt", 'a')
			fout.write(prevCon + " " + nextCon + " \n")
			fout.close()
	counter+=1

f.close()



