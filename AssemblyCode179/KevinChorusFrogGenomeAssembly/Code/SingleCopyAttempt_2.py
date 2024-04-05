import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]
outputFile2 = sys.argv[3]


# inputFile = "/home/kevin/Downloads/ForKevin/ccs1_15x4_wRC_100_Profiles.txt"
# outputFile = "/home/kevin/Downloads/ForKevin/SingleCopy.txt"
# outputFile2 = "/home/kevin/Downloads/ForKevin/SingleCopy2.txt"


numlines = 100000

#Thresholds

numBefore = 10
numAfter = 10
thresholdHigh = 1.0

numMiddle = 19
thresholdLow = 1.0

acceptalbeHighCoverage_UpperB = 17
acceptableHighCoverage_LowerB = 8

acceptalbeLowerCoverage_UpperB = 6
acceptableLowerCoverage_LowerB = 2




f = open(inputFile, 'r')

lstAll = []
lstLengths = []
lstCoverage = []

for i in range(0, numlines):

	print("Line: " + str(i))

	line = f.readline()
	sline = line.split("\t")
	lstLengths.append(len(sline))
	print(len(sline))

	lstReliable = []
	lstReliableCoverage = []
	flagEndOfLine = 0

	for j in range(0, (len(sline)-(numBefore+numMiddle+numAfter))):


		#Check that x% fall in between normal coverage for the next 10

		count = 0
		for k in range(0, numBefore):
			temp = int(sline[j+k])
			if (temp <= acceptalbeHighCoverage_UpperB and temp >= acceptableHighCoverage_LowerB):
				count+=1
		if (count*1.0)/(numBefore*1.0) >= thresholdHigh:
			pass
		else:
			continue


		#Check x% fall inbetween lower coverage  out of next 5
		count = 0
		for k in range(0, numMiddle):
			temp = int(sline[j + numBefore + k])
			if (temp <= acceptalbeLowerCoverage_UpperB and temp >= acceptableLowerCoverage_LowerB):
				count+=1
		if (count*1.0)/(numMiddle*1.0) >= thresholdLow:
			pass
		else:
			continue

		#While maintaining this x% coverage continue
		countextra = 0
		while ((count*1.0)/(numMiddle+countextra*1.0) >= thresholdLow):
			index = j + numBefore + numMiddle + countextra
			if index >= len(sline):
				flagEndOfLine = 1
				break
			temp = int(sline[index])
			if (temp <= acceptalbeLowerCoverage_UpperB and temp >= acceptableLowerCoverage_LowerB):
				count+=1
			countextra+=1

		#Check x% fall inbetween normal coverage after lower coverage for next 10
		count = 0
		for k in range(0, numAfter):
			index = j + numBefore + numMiddle + countextra+k
			if index >= len(sline):
				flagEndOfLine = 1
				break

			temp = int(sline[index])
			if (temp <= acceptalbeHighCoverage_UpperB and temp >= acceptableHighCoverage_LowerB):
				count+=1

		#Check if end of file has been reached
		if flagEndOfLine ==1:
			continue
				
		if (count*1.0)/(numAfter*1.0) >= thresholdHigh:
			pass
		else:
			continue		

		startIndex = j + numBefore
		stopIndex = j + numBefore + numMiddle + countextra



		lstTemp = []

		for k in range(startIndex, stopIndex):
			temp = int(sline[k])
			lstTemp.append(temp)

		modeLowCoverage = max(set(lstTemp), key=lstTemp.count)

		for k in range(startIndex, stopIndex):
			temp = int(sline[k])

			if (temp == modeLowCoverage):
				lstReliable.append(k)		


	lstAll.append(lstReliable)
	for j in range(0, len(lstReliable)):
		temp = int(sline[lstReliable[j]])
		lstReliableCoverage.append(temp)

	lstCoverage.append(lstReliableCoverage)
	#print(lstReliable)

f.close()





#print(lstAll)
f = open(outputFile, 'w')

for i in range(0, len(lstAll)):
	for j in range(0, len(lstAll[i])):
		f.write(str(lstAll[i][j]) + "\t")

	f.write("\n")
f.close()


f = open(outputFile2, 'w')

for i in range(0, len(lstCoverage)):
	for j in range(0, len(lstCoverage[i])):
		f.write(str(lstCoverage[i][j]) + "\t")

	f.write("\n")
f.close()



