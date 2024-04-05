inputHeaderFile = "ContigHeaders_MisjoinExamples.txt"

f = open(inputHeaderFile, 'r')

lstHeaders= []

for line in f:
	lstHeaders.append(line[:-1])

f.close()


outputdir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/ExampleMisjoinCoverage/"
inputfile = "PB.base.cov"
f = open(inputfile, 'r')


lstPBCoverage = []
header = ""
for line in f:
	#print(line)
	if len(line) < 1:
		continue
	if line[0] == ">":
		if lstPBCoverage != []:
			#print(lstPBCoverage)
			fout = open(outputdir + header + "_PBCoverage.txt", 'w', newline = "")
			for item in lstPBCoverage:
				fout.write(str(item) +" ")
			fout.close()
			lstPBCoverage = []
			header = ""


		sline = line.split()
		header = sline[0][1:]
		header = header + "_1"
		#print(header)
		#print(lstHeaders)
		if header in lstHeaders:
			length = int(sline[1])
			lstPBCoverage = [0]*length

	elif lstPBCoverage != []:
		sline = line.split()
		start = int(sline[0])
		stop = int(sline[1])
		cov = int(sline[2])
		lstPBCoverage[start-1:stop] = [cov]*((stop-start)+1)
f.close()
