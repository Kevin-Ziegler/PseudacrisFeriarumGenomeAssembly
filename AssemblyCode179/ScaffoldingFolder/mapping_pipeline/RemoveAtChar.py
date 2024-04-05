import sys



#inputFile = "tempFile.txt"

#outputFile = "tempFile_out.txt"

inputFile = sys.argv[1]
outputFile = sys.argv[2]


fin = open(inputFile, 'r')

fout = open(outputFile, 'w')


flagAfterHead = 0
counter = 0
for line in fin:
	
	if line[:3] == "@PG":
		flagAfterHead = 1
		fout.write(line)
		counter+=1
		continue

	if flagAfterHead == 1:
		line = line[1:]

	fout.write(line)

	if counter % 100000 == 0:
		print(counter)
	counter+=1
 

fout.close()
fin.close()


