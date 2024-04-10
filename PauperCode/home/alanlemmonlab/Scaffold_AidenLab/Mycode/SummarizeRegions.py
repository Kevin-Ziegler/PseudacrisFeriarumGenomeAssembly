#inputFile = "ListofRegionsToRemove.txt"
inputFile = "ListOfRegionsToRemove_PurgeMultiMap_3_20_2024_M.txt"

f = open(inputFile, 'r')


loci = 0
altered = 0
numBp = 0
totalDelete = 0
averageFragmentSize = 0
FragmentCount = 0
#AverageFragmentRemoved = 0
#AverageFragmentRemovedCount = 0


for line in f:
	l2 = f.readline()
	l3 = f.readline()
	loci+=1
	l3s = l3.split()
	if len(l3s) == 2:
		altered+=1
		l2s = l2.split()
		totalL = int(l2s[1])
		if l3s[0] == "0" and int(l3s[1]) == totalL:
			totalDelete+=1
		elif l3s[0] == "0":
			#print(totalL - int(l3s[1]))
			averageFragmentSize += (totalL - int(l3s[1]))
			FragmentCount+=1
		elif int(l3s[1]) == totalL:
			#print(int(l3s[0]))
			averageFragmentSize +=int(l3s[0])
			FragmentCount+=1
		else:
			#print(int(l3s[0]))
			#print(totalL - int(l3s[1]))
			averageFragmentSize +=int(l3s[0])
			averageFragmentSize += (totalL - int(l3s[1]))
			FragmentCount+=1
			FragmentCount+=1

		numBp = numBp + (int(l3s[1]) - int(l3s[0]))
print("Loci: " + str(loci/2))
print("Altered: " + str(altered/2))
print("TotalDeleted: " + str(totalDelete/2))
print("TotalSequence: " + str(numBp/2))
print("TotalFragments: " + str(FragmentCount/2))
averagefragmentRemoved = numBp/altered
print("Average FragmentSize Removed: " + str(averagefragmentRemoved))
averageFragmentSize = averageFragmentSize/FragmentCount
print("Average Remaining Fragment Size: " + str(averageFragmentSize))


