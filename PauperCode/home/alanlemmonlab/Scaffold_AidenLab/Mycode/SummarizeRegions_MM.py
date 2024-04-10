inputFile = "ListOfRegionsToRemove_PurgeMultiMap_3_20_2024.txt"

f = open(inputFile, 'r')


loci = 0
altered = 0
numBp = 0
totalDelete = 0
averageFragmentSize = 0
FragmentCount = 0
#AverageFragmentRemoved = 0
#AverageFragmentRemovedCount = 0

counter = 0
for line in f:

	l1 = f.readline()
	l2 = f.readline()
	l3 = f.readline()
	l3s = l3.split()
	l1s = l1.split()
	l2s = l2.split()

	if len(l3s) < 2:
		print(l3s)
		continue

	averageFragmentSize = averageFragmentSize + (int(l3s[1]) - int(l3s[0]))
	counter+=1

f.close()


print(averageFragmentSize/2)

averageFragmentSize = (averageFragmentSize/counter)/2

print(averageFragmentSize)
