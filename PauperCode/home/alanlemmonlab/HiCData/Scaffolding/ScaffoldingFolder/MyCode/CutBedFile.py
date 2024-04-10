import sys

bedFile = sys.argv[1]
percent = sys.argv[2]
newBedFileLocation = sys.argv[3]

f = open(bedFile,  'r')

countlines = 0

for line in f:
	countlines+=1
	if countlines % 10000000 == 0:
		print(countlines)

f.close()

print(countlines)


numLinesToGet = int(countlines * float(percent))

if numLinesToGet % 2 == 1:
	numLinesToGet = numLinesToGet + 1

print(numLinesToGet)

f = open(bedFile, 'r')
fout = open(newBedFileLocation, 'w')

countlines = 0
for line in f:
	if countlines == numLinesToGet:
		break

	fout.write(line)
	countlines+=1

f.close()
fout.close()


