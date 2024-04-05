inputNames = "stats_clip_HIC_GATC_v2_AGP_Add200.txt"
inputConnections = "VisHICScafwHICGATC.bsorted.pairs"
#inputConnections = "temp"
outFile = "matrixHIC_GATC"



f = open(inputNames, 'r')

lstNames = []
sizes = []

for line in f:
	sline = line.split()
	if len(sline) > 0:
		lstNames.append(sline[0])
		sizes.append(int(sline[1]))

f.close()

#print(lstNames)

matrix = []

for i in range(0, len(lstNames)):
	temp = []
	for j in range(0, len(lstNames)):
		temp.append(0)
	matrix.append(temp)


f = open(inputConnections, 'r')
dictIndex = {}

for i in range(0, len(lstNames)):
	dictIndex[lstNames[i]] = i

counter = 0

for line in f:
	if line[0] == "#" or len(line) < 3:
		counter +=1
		continue

	#print(line)
	sline = line.split()
	index1 = dictIndex[sline[1]]
	index2 = dictIndex[sline[3]]

	matrix[index1][index2] +=1
	matrix[index2][index1] +=1

	counter +=1
	if counter % 1000000 == 0:
		print(counter)

f.close()



fout = open(outFile + ".txt", 'w')
fout2 = open(outFile + "_Scaled.txt", 'w')

print("writing lists")

for i in range(0, len(matrix)):
	for j in range(0, len(matrix[i])):
		fout.write(str(matrix[i][j]) + " ")
		fout2.write(str(matrix[i][j] / (sizes[i] + sizes[j])) + " ")
	fout.write("\n")
	fout2.write("\n")

fout.close()
fout2.close()
