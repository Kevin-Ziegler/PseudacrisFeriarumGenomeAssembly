inputFile = "Combined_2.sam"

f = open(inputFile, 'r')

index = -1

hashmap = {}

counter = 0
for line in f:
	sline = line.split()
	#if counter == 74505:
	#	print("w"+sline[0]+"w")
	if "m54333U_200820_151308/1/0_1879" == sline[0]:
		print(counter)
		print(line)


	if counter % 100000 == 0:
		print(counter)
	counter+=1

f.close()

