inputFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/TestDifferentSCKmerThresholds/CovL_2_CovH_10_CovJump_2_DeltaLow_1_DeltaHigh_-1_Full/SCKmers_POS_delta.txt"

f = open(inputFile, 'r')

#stringF = "871	5327"
#stringF = "5666	7705"
stringF = "3354	7818"

counter = 0
for line in f:
	if stringF in line:
		print(counter)
	counter+=1

f.close()

