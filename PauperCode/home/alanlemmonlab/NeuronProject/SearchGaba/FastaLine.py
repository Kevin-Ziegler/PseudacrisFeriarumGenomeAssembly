fileName = "/home/alanlemmonlab/NeuronProject/Data/PferAssemblies/Trinity.fasta"

inLine = "TRINITY_DN16293_c0_g1_i3"

f = open(fileName, 'r')

for line in f:
	if inLine in line:
		print(line)
		line = f.readline()
		print(line)
f.close()
