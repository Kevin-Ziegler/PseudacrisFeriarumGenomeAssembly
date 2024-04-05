tableFile = "ProbesTable_Restriction_GATC_v2_2.txt"
#tableFile = "ProbesTable_Restriction_GATC_v2_First394.txt"
#tableFile = "temp"

#Name ProbeStart ProbeEnd ProbeScore GoodCoverage min max DistProbe Direction


f = open(tableFile, 'r')

lstProbeStartB = []
lstProbeStartE = []
lstProbeScore = []
lstGoodCoverage = []
listMin = []
listMax = []
listDistProbe = []

counter = 0
for line in f:
	if counter == 0:
		counter+=1
		continue
	sline = line.split()
	if "Begin" in sline[0]:
		lstProbeStartB.append(float(sline[1]))
	else:
		lstProbeStartE.append(float(sline[1]))

	lstProbeScore.append(float(sline[3]))
	lstGoodCoverage.append(float(sline[4]))
	listMin.append(float(sline[5]))
	listMax.append(float(sline[6]))
	listDistProbe.append(float(sline[7]))
	counter+=1

import matplotlib.pyplot as plt

#print(lstProbeStart)
plt.figure(0)
plt.hist(lstProbeStartB)
plt.title("Probe Location at Begining of Contig")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeStart_Begin.png")

plt.figure(6)
plt.hist(lstProbeStartE)
plt.title("Probe Location at End of Contig")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeStart_End.png")


plt.figure(1)
plt.hist(lstProbeScore, bins = 50, range = [0, 1000000])
plt.title("Probe Score")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeScore.png")

plt.figure(2)
plt.hist(lstGoodCoverage, bins = 50)
plt.title("Num Sites inbetween 80-120")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeGoodCoverage.png")

plt.figure(3)
plt.hist(listMin, bins = 25, range = [0, 1000])
plt.title("Lowest 21mer Coverage in Probe")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeMin.png")

plt.figure(4)
plt.hist(listMax, bins = 50, range = [0, 20000])
plt.title("Highest 21mer Coverager in Probe")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeMax.png")

plt.figure(5)
plt.hist(listDistProbe, bins = 50)
plt.title("Distance From Probe to GATC")
plt.savefig("/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/Probes_Restriction_GATC_Summary/ProbeDistanceStart.png")


