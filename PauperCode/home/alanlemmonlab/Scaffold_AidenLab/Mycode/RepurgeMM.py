def transformContigName(number):
	name = "tig"
	zeros = ""

	if number < 10:
		zeros = "0000000"
	elif number < 100:
		zeros = "000000"
	elif number < 1000:
		zeros = "00000"
	elif number < 10000:
		zeros = "0000"
	else:
		zeros = "000"

	return name + zeros + str(number) + "_1"

inputFile = "ListOfRegionsToRemove_PurgeMultiMap_3_20_2024.txt"
outFile = "ListOfRegionsToRemove_PurgeMultiMap_3_21_2024_Split.txt"

f = open(inputFile, 'r')


purgeWholeContig = 0.4
smallestFragmentSize = 15000

dictPurge = {}

dictFragment = {}


fout = open(outFile, 'w')


for line in f:
	l1 = f.readline()
	l2 = f.readline()
	l3 = f.readline()

	l1s = l1.split()
	l2s = l2.split()
	l3s = l3.split()

	stop = int(l3s[1])
	start = int(l3s[0])

	distance = stop - start
	smallerRegionSize = int(l2s[1])


	smallerContig = l2s[0]
	smallerContig = transformContigName(int(smallerContig))
	smallerContigSize = int(l2s[1])

	largerContig = transformContigName(int(l1s[0]))

	#if smallerRegionSize * .4 <= distance:
	#	dictPurge[smallerContig] = 1
	#	start = 0
	#	stop = smallerContigSize

	if start <= smallestFragmentSize:
		start = 0
	if (smallerContigSize - stop) <= smallestFragmentSize:
		stop = smallerContigSize

	fout.write(largerContig + " " + smallerContig + " \n")
	fout.write(smallerContig + " " +str(smallerContigSize) + " \n")
	fout.write(str(start) + " " + str(stop) + " \n")

fout.close()
f.close()
