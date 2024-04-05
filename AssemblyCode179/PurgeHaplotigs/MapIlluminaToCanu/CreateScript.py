
def changeR1_R2(read1):
	lastChar = ""
	newR2 = ""
	for item in read1:
		if lastChar + item == "R1":
			newR2 = newR2 + "2"
		else:
			newR2 = newR2 + item
		lastChar = item

	return newR2


inputR1Files = "/pool/PacBioAssembly/PE250/AllRead1Names.txt"


fR1 = open(inputR1Files, 'r')

command = "nohup bwa mem -t 60 CanuContigsBWA "

#<(cat A.read1.fq B.read1.fq ...)

R1 = "<(cat "
R2 = "<(cat "

loc = "/pool/PacBioAssembly/PE250"

count = 0
for item in fR1:

	R1 = R1 + loc + item[1:-1] + " "
	temp = changeR1_R2(item)
	R2 = R2 + loc + temp[1:-1] + " "

	if count == 5:
		#break
		pass
	count+=1

R1 = R1 + ") "
R2 = R2 + ")"


command = command + R1 + R2 + " > BWAPE1.out 2> BWAPE1.err & "
print(command)
