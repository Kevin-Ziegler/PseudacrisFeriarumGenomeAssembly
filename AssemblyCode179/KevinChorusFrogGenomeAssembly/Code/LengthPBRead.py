#inputFile = "/pool/PacBioAssembly/CCS/ccs1.fasta"
inputFile = "/pool/PacBioAssembly/CCS/ccs1.2bit"

f = open(inputFile, 'r')

#lineNum = 427571*2+1
lineNum = 427571

counter = 0
for line in f:
	if counter == lineNum:
		print(len(line))
	counter+=1

f.close()
