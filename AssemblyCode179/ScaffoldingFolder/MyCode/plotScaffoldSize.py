#import matplotlib.pyplot as plt

#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingFolder/SALSA-master/scaffolds/scaffold_length_iteration_5"
#inputFileName = "scaffold_length_iteration_5_HIC"
#inputFileName = "scaffold_length_iteration_5"
#12.5%
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/HiC_12_5Percent/scaffold_length_iteration_5"
#25%
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/HiC_25_Percent/scaffold_length_iteration_5"
#50%
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/HiC_50_Percent/scaffold_length_iteration_5"
#Full
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingFolder/SALSA-master/scaffoldsHiC/scaffold_length_iteration_5_HIC"

#TrimmedDataSetChicago
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedChicago/scaffold_length_iteration_5"
#inputFileName = "stats2.txt"

#TrimmedHiC
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedHIC/scaffold_length_iteration_5"
#inputFileName = "stats_HIC.txt"
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/PurgeHaplotigs/MapIlluminaToCanu/stats_clip.txt"

#Haplotype 1 Chicago 
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingFolder/SALSA-master/scaffoldsHaplotype/scaffold_length_iteration_5"

#Purged Assembly v2
#inputFileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/PurgedContigLengths.txt"
inputFileName = ""

outputFileName = ""

inputFile = open(inputFileName, 'r')

lstLength = []

for line in inputFile:
	sline = line.split()
	if len(sline) >= 2:
		lstLength.append(int(sline[1]))
		

#plt.hist(lstLength, bins=20, log = True)
#plt.savefig('ScaffoldLength_HIC.png')
#plt.show()
#plt.close()

sumlist = sum(lstLength)
print(sumlist)

lstLength.sort(reverse=True)

runningsum = 0
countNG = .5
for i in range(0, len(lstLength)):
	item = lstLength[i]
	
	if runningsum >= sumlist* countNG:
	#if runningsum > 4000000000 * .9:
		print("NG " + str(countNG* 100) + ": " + str(item))
		print("In Pieces: " + str(i))
		countNG = countNG + 0.1
		
	
	runningsum = runningsum + item

print("NG " + str(countNG* 100) + ": " + str(item))
print("In Pieces: " + str(i))

print(lstLength[0:100])
