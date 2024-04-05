import matplotlib.pyplot as plt

def passAbsoluteMinMax(listCoverage, minVal, maxVal, probe):
	templist = listCoverage[probe[0]:probe[1]]
	mint = min(templist)
	maxt = max(templist)
	if mint > minVal and maxt < maxVal:
		return 1
	return 0

def scoreProbe(coverage, avgCoverage):
	if coverage > avgCoverage:
		probeScore = (coverage - avgCoverage)
	elif coverage > avgCoverage/2:
		probeScore =  (avgCoverage - coverage) *2
	else:
		probeScore = (avgCoverage - coverage)**2

	return probeScore

def checkWithRangeRE(listRE, pos, threshold, probeLength):
	probeStart = pos
	probeEnd = pos+probeLength

	#Check if there are any RE sites in the probe
	for i in range(0, len(listRE), 2):
		if probeStart <= listRE[i] and probeEnd > listRE[i]:
			return [1,0]
		if probeStart < listRE[i+1] and probeEnd >= listRE[i+1]:
			return [1,0]

	#If not find closest stop and start point
	distStart = 99999
	distStop = 99999
	for i in range(0, len(listRE), 2):
		if (probeEnd < listRE[i]) and ((listRE[i] - probeEnd) < distStop) :
			distStop = listRE[i] - probeEnd

		if (probeStart > listRE[i+1]) and ((probeStart - listRE[i+1]) < distStart) :
			distStart = probeStart - listRE[i+1]

		if (listRE[i]) > (500+probeStart):
			break
	smallerDist = -1
	stopStart = ""
	if distStart < distStop:
		smallerDist = distStart
		stopStart = "Forward"
	else:
		smallerDist = distStop
		stopStart = "Reverse"

	if smallerDist <= threshold:
		return [0,smallerDist, stopStart]

	return [1,0]

def checkIfMask(listMask, pos, probeLength):
	start = 0
	stop = 0
	for i in range(0, len(listMask), 2):
		start = listMask[i]
		stop = listMask[i+1]

		if pos > start and pos < stop:
			return 1
		if (pos+probeLength) > start and (pos+probeLength) < stop:
			return 1
	return 0

def checkIfNearOtherProbe(pos, lstOtherProbes, threshold):
	for i in range(0, len(lstOtherProbes)):
		if abs(lstOtherProbes[i][0] - pos) < threshold:
			return 1
	return 0



def findProbe(listCoverage, listRE, smask, otherProbes):

	probe = [0,0]
	probeLength = 120
	#percentSingleCov = 0.6
	threshold_High = 120
	threshold_Low = 80
	#minVal = 20
	#maxVal = 10000
	avgCoverage = 100
	thresholdProbe = 200
	distanceFromOtherProbes = 200
	distanceFromREPenaltyPerSite = 1000

	probeScore = 0
	#lowest = 10000
	highest = 0
	maxProbeScore = 100000000000
	dist = 9999
	direction = ""

	#Find first 120 bp
	numInThreshold = 0
	for i in range(0, probeLength):
		probeScore = probeScore + scoreProbe(listCoverage[i], avgCoverage)


	#update score iterating over bp of the rest of the list
	for i in range(probeLength, len(listCoverage)):
		probeScore = probeScore + scoreProbe(listCoverage[i], avgCoverage)
		probeScore = probeScore - scoreProbe(listCoverage[i-probeLength], avgCoverage)

		checkRE = checkWithRangeRE(listRE, i-probeLength, thresholdProbe, probeLength)
		acceptableProbeRE = checkRE[0]
		probeScoreDistanceFromRE = 0
		if acceptableProbeRE == 0:
			probeScoreDistance = checkRE[1] * distanceFromREPenaltyPerSite
		else:
			continue

		if (maxProbeScore > (probeScore + probeScoreDistance)) and (checkIfMask(smask, i-probeLength, probeLength) == 0) and (checkIfNearOtherProbe(i-probeLength, otherProbes, distanceFromOtherProbes) == 0):
			probe[1] = i
			probe[0] = i-probeLength
			maxProbeScore = probeScore + probeScoreDistance
			dist = checkRE[1]
			direction = checkRE[2]

	if probe[0] == 0 and probe[1] == 0:
		return "NoProbe"
	probeList = listCoverage[probe[0]:probe[1]]
	#print("Probe List")
	#print(probe)

	goodCoverage = 0
	for i in range(0, len(probeList)):
		if probeList[i] < threshold_High and probeList[i] > threshold_Low:
			goodCoverage+=1
	#print("found probe")
	#print(probeList)
	pmin = min(probeList)
	#print(probeList)
	pmax = max(probeList)

	return [probe, maxProbeScore, goodCoverage, pmin, pmax, dist, direction]

#fileHeaders = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/HeadersForCoverageAll.txt"
#fileCoverage = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/CoverageForCoverageAll.txt"
#fileMaskCoords = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/AlanMasker/RunD_100_MaskCoords.txt"
#fileRestrictionSites = "RestrictionSites_GATC.txt"

fileHeaders = "Contig_v2_Coverage2_Headers.txt"
fileCoverage = "Contig_v2_Coverage2_Coverage.txt"
fileMaskCoords = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/AlanMasker/Contig_v2_2_MaskCoords.txt"
fileRestrictionSites = "RestrictionSites_GATC.txt"


numFoundProbes = 0
ProbesPerContigEnd = 2

fHeader = open(fileHeaders, 'r')
fCov = open(fileCoverage, 'r')
fMask = open(fileMaskCoords, 'r')
fRestriction = open(fileRestrictionSites, 'r')

fout = open("ProbesTable_Restriction_GATC_v2_2.txt", 'w')
fout.write("Name ProbeStart ProbeEnd ProbeScore GoodCoverage min max DistProbe Direction\n")


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
for i in range(0, counter*2):
	print(i)
	if i%2 == 0:
		header = fHeader.readline()
		direction = "Begin"
	else:
		direction = "End"
	coverage = fCov.readline()
	restrictionSites = fRestriction.readline()
	mask = fMask.readline()
	scoverage = coverage.split()
	smask = mask.split()
	sRestriction = restrictionSites.split()
	for j in  range(0, len(scoverage)):
		scoverage[j] = float(scoverage[j])
	for j in range(0, len(smask)):
		smask[j] = float(smask[j])
	for j in range(0, len(sRestriction)):
		sRestriction[j] = int(sRestriction[j])
	smask = smask[1:]
	#sRestriction = sRestriction[:-1]
	#print(smask)
	#print(len(smask))


	#find probes
	if len(scoverage) == 0 or len(sRestriction) == 0:
		continue

	currentProbes = []
	for p in range(0, ProbesPerContigEnd):
		out = findProbe(scoverage, sRestriction, smask, currentProbes)
		if out == "NoProbe":
			print("No Probe")
			continue
		probe = out[0]
		score = out[1]
		goodCoverage = out[2]
		pmin = out[3]
		pmax = out[4]
		dist = out[5]
		directionProbe = out[6]

		currentProbes.append(probe)

		#plt.figure()
		#plt.title(header[:-1])
		#plt.plot(lstX, scoverage, 'k', markersize=.1, label = "Coverage")
		#for j in range(0, len(smask),2):
		#	start = int(smask[j])
		#	stop = int(smask[j+1])
		#	xcoord = lstX[start:stop]
		#	ycoord = scoverage[start:stop]
			#xcoord = []
			#ycoord = []
			#xcoord.append(lstX[start])
			#xcoord.append(lstX[stop])
			#ycoord.append(scoverage[start])
			#ycoord.append(scoverage[stop])

		#	if j == 0:
				#plt.plot(xcoord, ycoord, 'r', markersize=.1, label = "Mask")
		#	else:
				#plt.plot(xcoord, ycoord, 'r', markersize=.1)
		if probe[1] != 0:
			#plt.plot(lstX[probe[0]:probe[1]], scoverage[probe[0]:probe[1]], 'orange', label = "Probe")
			numFoundProbes+=1


		#for j in range(0, len(sRestriction),2):
			#print(sRestriction[j])
			#print(sRestriction[j+1])
			#print(lstX[sRestriction[j]:sRestriction[j+1]])
			#print(scoverage[sRestriction[j]:sRestriction[j+1]])
		#	if j == 0:
				#plt.plot(lstX[sRestriction[j]:sRestriction[j+1]], scoverage[sRestriction[j]:sRestriction[j+1]], 'green', label = "RestrictionSites")
		#	else:
				#plt.plot(lstX[sRestriction[j]:sRestriction[j+1]], scoverage[sRestriction[j]:sRestriction[j+1]], 'green')


		#plt.legend()
		#plt.yscale('log')
		#plt.savefig("Examples/Probes_Restriction_GATC/" + header[:-1]+ "_" + direction + "_Probe_" + str(p+1) + ".png")
		#plt.xlim([probe[0]-200, probe[1]+200])
		#plt.savefig("Examples/Probes_Restriction_GATC/" + header[:-1]+ "_" + direction + "_Probe_" + str(p+1) + "_Zoom.png")

		#plt.close()

		fout.write(header[:-1]+ "_" + direction + " " + str(probe[0]) + " " + str(probe[1]) + " " + str(score) + " " + str(goodCoverage) + " " + str(pmin) + " " + str(pmax) + " " + str(dist) + " " + str(directionProbe) + " \n")

		#if( i >= 40):
		#	print(numFoundProbes)
		#	print(i)
		#	break

#print(numFoundProbes)
#print(counter)

fHeader.close()
fCov.close()
fMask.close()

