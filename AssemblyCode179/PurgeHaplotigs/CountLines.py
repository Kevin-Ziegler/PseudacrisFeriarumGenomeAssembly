inputFile = "Combined_2.sam"

f = open(inputFile, 'r')

index = -1

hashmap = {}

counter = 0
for line in f:
	counter+=1

	if counter >= 74500 and counter <= 74510:
		print(line)

	if counter >= 57661860 and counter <= 57661870:
		print(line)

	if counter % 100000 == 0:
		print(counter)
f.close()
