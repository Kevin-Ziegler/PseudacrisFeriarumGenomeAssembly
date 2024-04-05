fileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ChorusFrog_Canu_CLR_2/Canu_Contig_Headers.txt"

f = open(fileName, 'r')

name = []
length = []
repeat = []
numReads = []
coverage = []


counter = 0
for line in f:
	sline = line.split()
	name.append(sline[0][1:])
	length.append(sline[1][4:])
	repeat.append(sline[4][14:])
	#break
	counter+=1
	#if counter == 10:
	#	break

f.close()

print(name)
print(length)
print(repeat)


fileName2 = "ReadsMappedToContigs.txt"

f2 = open(fileName2, 'r')


counter2 = 0
for line in f2:
	sline = line.split()
	tempName = sline[0]
	tempReadDepth = sline[1]

	if tempName == name[counter2]:
		numReads.append(tempReadDepth)
		coverage.append(float(tempReadDepth)/float(length[counter2]) * 250)
	else:
		numReads.append(0)
		numReads.append(0)
	counter2+=1
f2.close()



outFile = "Coverage.txt"

of = open(outFile, 'w')

avgrepeat = 0
rc = 0
avgnormal = 0
nc = 0

covhigh = 0
covhighMult = 0

sumCov_ReadLength = 0
readLengthHighCov = 0

for i in range(0, len(name)):
	of.write(name[i] + " " + str(numReads[i]) + " " + str(coverage[i]) + " " + str(length[i]) + " " + repeat[i] + " \n")
	if repeat[i] == "yes":
		avgrepeat = avgrepeat + coverage[i]
		rc+=1
	else:
		avgnormal = avgnormal + coverage[i]
		nc+=1

	if coverage[i] > 300:
		print(name[i] + " " + str(numReads[i]) + " " + str(coverage[i]) + " " + str(length[i]) + " " + repeat[i] + " \n")
		covhigh+=1
		if int(length[i]) > 15000:
			covhighMult = covhighMult + float(coverage[i])/100.0
		sumCov_ReadLength = sumCov_ReadLength + float(coverage[i])/100.0 * float(length[i]) 
		readLengthHighCov = readLengthHighCov + float(length[i])
	#if coverage[i] >= 200:
	

	
of.close()


print(avgrepeat/rc)
print(avgnormal/nc)
print(covhigh)


print(readLengthHighCov)
print(sumCov_ReadLength)
print(covhighMult)
