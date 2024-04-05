fileName = "clip.fasta"

f = open(fileName, 'r')

names=[]
length = []

countchar = 0

for line in f:
	if  ">" in line:
		names.append(line[1:-1])
	else:
	
