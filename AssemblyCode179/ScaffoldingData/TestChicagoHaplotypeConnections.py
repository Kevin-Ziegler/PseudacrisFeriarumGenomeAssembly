inputFile = "Pfer_alignment.bed"
#inputFile = "test"

f = open(inputFile, 'r')

hashmap = {}

counter = 0
countMoreThanOnce = 0

indexStop = -1

for line in f:
	sline = line.split()
	chicagoName = sline[3][:-2]
	#print(chicagoName)
	if chicagoName in hashmap:
		if hashmap[chicagoName] == 2:
			countMoreThanOnce +=1
		hashmap[chicagoName] = hashmap[chicagoName] + 1
	else:
		hashmap[chicagoName] = 1

	counter +=1
	if counter == indexStop:
		break

	if counter % 1000000 == 0:
		print(str(counter) + " " + str(countMoreThanOnce))

countMoreThanOnce = 0
print(len(hashmap))
for key in hashmap:
	if hashmap[key] != 2:
		countMoreThanOnce +=1
print(countMoreThanOnce)
