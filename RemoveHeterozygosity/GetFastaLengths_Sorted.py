import sys

fastaFile = sys.argv[1]
lengthsFile = sys.argv[2]


f = open(fastaFile, 'r')
fout = open(lengthsFile, 'w')

length = ""
seq = ""

lst =[]

for line in f:
	if ">" in line:
		length = str(len(seq))

		if seq != "":
			#fout.write("Sequence ID: " + header + " Length: " + length + " \n")
			temp = [header, int(length)]
			lst.append(temp)

		header = line[1:].strip()
		seq = ""
	else:
		seq = seq + line.strip()

length = str(len(seq))

if seq != "":
	#fout.write("Sequence ID: " + header + " Length: " + length + " \n")
	temp = [header, int(length)]
	lst.append(temp)


f.close()

sortedlst = sorted(lst, key= lambda x: x[1], reverse=True)
for i in range(0, len(sortedlst)):
	fout.write(">" + sortedlst[i][0] + " " + str(i+1) + " " + str(sortedlst[i][1]) + " \n")

fout.close()

print(len(sortedlst) + 100000)
