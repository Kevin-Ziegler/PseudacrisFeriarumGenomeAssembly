import pickle
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


inputLst = "dataCoords.pickle"
inputContigLengths = "ContigLengths.txt"
output = "ListOfRegionsToRemove_PurgeMultiMap.txt"

minSpan = 20000
minDistanceCovered = 0.20
minDistanceToCountBetweenPoints = 10000
distanceFromMedian = 6.0


discardWholeRegion = 0.4


dictContigLen = {}

f = open(inputContigLengths, 'r')

for line in f:
	sline = line.split()
	if len(sline) > 0:
		parsename = int(sline[0][4:-2])
		parsename = str(parsename)
		dictContigLen[parsename] = int(sline[2])

f.close()

#print(dictContigLen)


fout = open(output, 'w')


with open(inputLst, "rb") as file:
	loaded_data = pickle.load(file)



counterT=0

for i in range(0, len(loaded_data)):
	if len(loaded_data[i]) > 0:
		print("index", i)
		#print(loaded_data[i])
		for item in loaded_data[i]:
			print("subitem", item)
			x = loaded_data[i][item]
			y = loaded_data[item][i]

			numreads = len(x)

			xlen = dictContigLen[str(i)]
			ylen = dictContigLen[str(item)]

			smaller = 0
			larger = 0

			if xlen <= ylen:
				smaller = i
				larger = item
			else:
				smaller = item
				larger = i

			smallerpoints = loaded_data[smaller][larger]
			smallerSize = dictContigLen[str(smaller)]
			largerSize = dictContigLen[str(larger)]

			smallest = min(smallerpoints)
			largest = max(smallerpoints)
			#Smaller than 20kb
			if (largest-smallest) <= minSpan:
				print("Failed: Less than 20kb ")
				continue

			sortedSmallPoints = sorted(smallerpoints)
			distanceCovered = 0

			for j in range(0, len(sortedSmallPoints)-1):
				tempDist = sortedSmallPoints[j+1] - sortedSmallPoints[j]
				if tempDist < minDistanceToCountBetweenPoints:
					distanceCovered = distanceCovered + tempDist

			#Less than 20% of the region is "aligned" or "covered" by the heterozygous reads
			if distanceCovered < (minDistanceCovered * smallerSize):
				#continue
				print("Failed: Region not covered enough")
				continue

			medianIndex = int(len(sortedSmallPoints)/2)
			median = sortedSmallPoints[medianIndex]
			averageDistanceFromMedian = 0

			for j in range(0, len(sortedSmallPoints)):
				averageDistanceFromMedian = averageDistanceFromMedian + abs(median - sortedSmallPoints[j])
			averageDistanceFromMedian = averageDistanceFromMedian/len(sortedSmallPoints)

			trimleft = 0
			trimright = 0

			for j in range(0, len(sortedSmallPoints)):
				if abs(sortedSmallPoints[j] - median) > (distanceFromMedian * averageDistanceFromMedian):
					continue
				else:
					trimleft = sortedSmallPoints[j]
					break


			for j in range(len(sortedSmallPoints)-1, -1, -1):
				if abs(sortedSmallPoints[j] - median) > (distanceFromMedian * averageDistanceFromMedian):
					continue
				else:
					trimright = sortedSmallPoints[j]
					break

			#print(smallest)
			#print(largest)
			#print(trimleft)
			#print(trimright)
			#print(median)
			#print(averageDistanceFromMedian)
			fout.write("Start \n")
			fout.write(str(larger) + " " + str(largerSize) + " \n")
			fout.write(str(smaller) + " " + str(smallerSize) + " \n")
			fout.write(str(trimleft) + " " + str(trimright) + " \n")

			if counterT % 100 ==0:
				fout.flush()
			counterT+=1


			#print(i)
			#plt.plot(x,y, 'bo')
			#plt.title("Contig: " + str(i) + " Contig: " + str(item) + " Connections: " + str(numreads))
			#plt.xlim([0, xlen])
			#plt.ylim([0, ylen])
			#plt.show()
fout.close()
