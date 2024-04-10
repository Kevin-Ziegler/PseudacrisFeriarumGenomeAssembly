import sys

fastaFile = sys.argv[1]
numFiles = int(sys.argv[2])
outputDirc = sys.argv[3]
outputStem = sys.argv[4]

lst_file_objects = []

for i in range(0, numFiles):
	temp = open(outputDirc + outputStem + str(i) + ".fasta", 'w')
	lst_file_objects.append(temp)

fin = open(fastaFile, 'r')

lineNum = 0
countFile = 0
for line in fin:
	if ">" in line:
		templine = line[10:]
		templine = templine[:-7]
		scaffoldNum = int(templine)
		#print(scaffoldNum)
		outf = lst_file_objects[scaffoldNum % numFiles]
		countFile+=1
		outf.write(line)
	else:
		outf.write(line)

for i in range(0, numFiles):
	temp = lst_file_objects[i]
	temp.close()
fin.close()



