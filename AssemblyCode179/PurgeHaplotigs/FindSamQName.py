inputFile = "align2.sam"

f = open(inputFile, 'r')

index = -1

hashmap = {}

counter = 0
for line in f:
	sline = line.split()
	if sline[0] in hashmap:
		hashmap[sline[0]] = hashmap[sline[0]] + 1
	else:
		hashmap[sline[0]] = 1
	#print(sline[0] + " " + sline[2] + " " + sline[3])
	counter+=1

	if counter % 100000 == 0:
		print(counter)
f.close()


print(len(hashmap))
