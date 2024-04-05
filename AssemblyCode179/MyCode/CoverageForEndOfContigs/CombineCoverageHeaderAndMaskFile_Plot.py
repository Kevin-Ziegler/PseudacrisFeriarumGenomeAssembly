import matplotlib.pyplot as plt

def passAbsoluteMinMax(listCoverage, minVal, maxVal, probe):
	templist = listCoverage[probe[0]:probe[1]]
	mint = min(templist)
	maxt = max(templist)
	if mint > minVal and maxt < maxVal:
		return 1
	return 0

def findProbe(listCoverage):

	probe = [0,0]
	probeLength = 120
	percentSingleCov = 0.6
	threshold_High = 120
	threshold_Low = 80
	minVal = 20
	maxVal = 10000

	probeScore = 0
	lowest = 10000
	highest = 0


	#Find first 120 bp
	numInThreshold = 0
	for i in range(0, probeLength):
		if listCoverage[i] <= threshold_High and listCoverage[i] >= threshold_Low:
			numInThreshold+=1
		#if listCoverage[i] > highest:
		#	highest = listCoverage[i]
		#if listCoverage[i] < lowest:
		#	lowest = listCoverage[i]

	#First 120 bp works
	if numInThreshold > (percentSingleCov * probeLength) and passAbsoluteMinMax(listCoverage, minVal, maxVal, [0,119]) == 1:
		probe[1] = 119
		probeScore = numInThreshold

	#update score iterating over bp of the rest of the list
	for i in range(probeLength, len(listCoverage)):
		if listCoverage[i] <= threshold_High and listCoverage[i] >= threshold_Low:
			numInThreshold+=1

		if listCoverage[i-probeLength] <= threshold_High and listCoverage[i-probeLength] >= threshold_Low:
			numInThreshold-=1

		if numInThreshold > (percentSingleCov * probeLength) and passAbsoluteMinMax(listCoverage, minVal, maxVal, [i-probeLength,i]) == 1:

			if numInThreshold > probeScore:
				probe[1] = i
				probe[0] = i-probeLength
				probeScore = numInThreshold
	return probe

fileHeaders = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/HeadersForCoverageAll.txt"
fileCoverage = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/CoverageForCoverageAll.txt"
fileMaskCoords = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/AlanMasker/RunD_100_MaskCoords.txt"


probeLength = 120
percentSingleCov = 0.6
threshold_High = 120
threshold_Low = 80


numFoundProbes = 0

fHeader = open(fileHeaders, 'r')
fCov = open(fileCoverage, 'r')
fMask = open(fileMaskCoords, 'r')


counter = 0
for line in fHeader:
	counter+=1
fHeader.close()
fHeader = open(fileHeaders, 'r')

lstX = []
for i in range(0, 10000):
	lstX.append(i+1)

header = ""
direction = ""
for i in range(0, counter):
	print(i)
	if i%2 == 0:
		header = fHeader.readline()
		direction = "Begin"
	else:
		direction = "End"
	coverage = fCov.readline()
	mask = fMask.readline()
	scoverage = coverage.split()
	smask = mask.split()
	for j in  range(0, len(scoverage)):
		scoverage[j] = float(scoverage[j])
	for j in range(0, len(smask)):
		smask[j] = float(smask[j])
	smask = smask[1:]
	#print(smask)
	#print(len(smask))


	#find probes
	probe = findProbe(scoverage)

	plt.figure()
	plt.title(header[:-1])
	plt.plot(lstX, scoverage, 'k', markersize=.1, label = "Coverage")
	for j in range(0, len(smask),2):
		start = int(smask[j])
		stop = int(smask[j+1])
		xcoord = lstX[start:stop]
		ycoord = scoverage[start:stop]
		#xcoord = []
		#ycoord = []
		#xcoord.append(lstX[start])
		#xcoord.append(lstX[stop])
		#ycoord.append(scoverage[start])
		#ycoord.append(scoverage[stop])

		if j == 0:
			plt.plot(xcoord, ycoord, 'r', markersize=.1, label = "Mask")
		else:
			plt.plot(xcoord, ycoord, 'r', markersize=.1)

	if probe[1] != 0:
		plt.plot(lstX[probe[0]:probe[1]], scoverage[probe[0]:probe[1]], 'orange', label = "Probe")
		numFoundProbes+=1

	plt.legend()
	plt.yscale('log')
	plt.savefig("Examples/Probes_Mask/" + header[:-1]+ "_" + direction + ".png")
	plt.close()

	if( i == 1000):
		print(numFoundProbes)
		print(i)
		break

#print(numFoundProbes)
#print(counter)

fHeader.close()
fCov.close()
fMask.close()

