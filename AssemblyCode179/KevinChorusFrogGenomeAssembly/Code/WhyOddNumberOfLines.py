file = "/pool/PacBioAssembly/CCS/ccs1.fasta"
#file = "test.txt"


f = open(file, 'r')


flagCarrot = 0
lineNum = 0


for line in f:
	newflagCarrot = -1
	
	if ">" in line:
		newflagCarrot = 1
	else:
		newflagCarrot = 0
	
	if flagCarrot == newflagCarrot:
		print("Werid")
		print(lineNum)		

	flagCarrot = newflagCarrot

	lineNum+=1

f.close()

print(lineNum)
