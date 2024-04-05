subFiles = 50

sample = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CoverageForEndOfContigs/Examples/FastaSubFiles/temp_"



beginCommand  = "python coverage_contigs_v2.py "

for i in range(0, subFiles):
	command = beginCommand + sample + str(i) + ".fasta " + sample + str(i) + "_Coverage.fasta"

	print(command)


