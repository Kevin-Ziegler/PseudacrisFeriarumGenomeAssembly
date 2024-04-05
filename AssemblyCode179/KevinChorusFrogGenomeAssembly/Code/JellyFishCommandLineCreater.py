inputFile = "/pool/PacBioAssembly/PE250/ListAllPEFastaFiles.txt"

f = open(inputFile, 'r')

lstFiles = []

for line in f:
	lstFiles.append(line[:-1])

f.close()


CmdLineJelly = "jellyfish-2.3.0/bin/jellyfish count -m 21 -s 46000000000 -t 64 -C "
cmd2 = "-o reads_All_21.jf"

for i in range(0, len(lstFiles)):
	CmdLineJelly = CmdLineJelly + lstFiles[i] + " " 

CmdLineJelly = CmdLineJelly + cmd2

print(CmdLineJelly)
