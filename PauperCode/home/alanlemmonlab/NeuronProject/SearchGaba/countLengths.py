file = "../Results/TestGaba/TRINITY_DN125889_c0_g1_i1.fasta"

f = open(file, 'r')

for line in f:
	print(len(line))

f.close()
