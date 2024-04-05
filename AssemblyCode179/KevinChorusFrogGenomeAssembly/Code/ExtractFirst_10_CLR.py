inputFile = "/pool/PacBioAssembly/CLR/PacBio_CLR_Subreads_Well1.fasta"
outputFile = "/pool/PacBioAssembly/CLR/First_10_CLR_100000.fasta"

f = open(inputFile, 'r')

fout = open(outputFile, 'w')

templine = ""
counter = 0


for line in f:
	templine = line
	line = f.readline()
	
	#print(len(line))
	if len(line) > 100000:
		fout.write(templine)
		fout.write(line)
		print(counter)
		print(len(line))
		
		
		counter+=1

		if counter == 10:
			break
fout.close()
f.close()
