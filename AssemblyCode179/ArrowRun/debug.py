fileName = "TryBioStars/test"

f = open(fileName, 'r')

counter = 0
for line in f:
	sline = line.split()
	if sline[2] == "scaffold_10":
		print(counter)
	counter+=1

	if counter % 1000 == 0:
		print(counter)

f.close()
