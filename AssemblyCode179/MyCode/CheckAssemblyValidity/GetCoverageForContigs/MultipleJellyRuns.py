#inputHeaderFile = "AnuranDupsContigHeaders.txt"

inputHeaderFile = "ContigHeaders_MisjoinExamples.txt"

f = open(inputHeaderFile, 'r')
fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged.fa"
#fasta_file = "Testfasta.fa"
jellyfish_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/KevinChorusFrogGenomeAssembly/reads_All_21.jf"




#outputdirc="/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/AnuranDups/"
outputdirc = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/ExampleMisjoinCoverage/"

for line in f:
	if len(line) > 1:
		command = "python CheckAlignmentCoverageBasedOnJelly_GPT.py " + fasta_file + " " + jellyfish_file + " " + line[:-1] + " " + outputdirc
		print(command)

f.close()
