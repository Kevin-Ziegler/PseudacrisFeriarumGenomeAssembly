import sys

fastaFile = sys.argv[1]
lengthsFile = sys.argv[2]


f = open(fastaFile, 'r')
fout = open(lengthsFile, 'w')

length = ""
seq = ""
for line in f:
	if ">" in line:
		length = str(len(seq))

		if seq != "":
			fout.write("Sequence ID: " + header + " Length: " + length + " \n")

		header = line[1:].strip()
		seq = ""
	else:
		seq = seq + line.strip()

length = str(len(seq))

if seq != "":
	fout.write("Sequence ID: " + header + " Length: " + length + " \n")


f.close()
fout.close()
