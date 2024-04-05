inputFile = "RunD_100_VerifyInR.r"
numSubFiles = 25
perFile = 1000

f = open(inputFile, 'r')

lstSubFiles = []

for i in range(0, numSubFiles):
	fout = open("SubFilesPlot/plot_1000_" +str(i) + ".r", 'w')
	lstSubFiles.append(fout) 

counter = 0
for line in f:
	if counter == 0:
		for i in range(0, len(lstSubFiles)):
			lstSubFiles[i].write('pdf("SubFilesPlot/AlanMasker_repeatMap_' + str(i) + '.pdf")\n')
	elif counter ==1:
		for i in range(0, len(lstSubFiles)):
			lstSubFiles[i].write('plot(-9999,-9999,xlim=c(0,1000),ylim=c(' + str(i * 1000)+ ',' + str((i+1) *1000)+  '),main="/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/CoverageForCoverageAll.txt",xlab="Site",ylab="Locus")\n')
	elif counter == 2:
		for i in range(0, len(lstSubFiles)):
			lstSubFiles[i].write('rect(0,-15,10000,25000,col="black")\n')
	elif counter >=1 and counter <=10:
		for i in range(0, len(lstSubFiles)):
			lstSubFiles[i].write(line)
	else:
		#print(line)
		sline = line.split(",")
		if len(sline) < 3:
			continue
		contigNum = int(sline[3][:-1])
		file = int(contigNum/perFile)
		#print(contigNum)
		#print(file)
		lstSubFiles[file].write(line)
	counter+=1


for i in range(0, len(lstSubFiles)):
	lstSubFiles[i].write("dev.off()")
	lstSubFiles[i].close()
f.close()
