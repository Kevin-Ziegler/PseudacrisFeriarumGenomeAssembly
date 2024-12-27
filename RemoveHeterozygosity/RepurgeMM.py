#The purpose of this file is to take the list of candidate areas to remove and modify them.
#The modification is ensuring small segmenets are not removed. 

import sys

#input file of regions. Output from MultiMapRemove.py
#inputFile = "ListOfRegionsToRemove_PurgeMultiMap.txt"
inputFile = sys.argv[1]

#new filename of list of candidate regions to remove
#outFile = "ListOfRegionsToRemove_PurgeMultiMap_Split.txt"
outFile = sys.argv[2]

#minimum size of segment to remove from contig
smallestFragmentSize = 15000

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

f = open(inputFile, 'r')


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
