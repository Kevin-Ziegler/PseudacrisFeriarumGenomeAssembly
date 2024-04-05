cores = 30
numberFiles = 60

stemOfFile = "scaffolds_v2_GATC_Arrow_2_split"
backFile = ".maker.output"
baseDirectory = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/Transfer/"

maker2zff = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/maker/bin/maker2zff"
options = " -x 0.25 -l 50 -d "

tempDir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/snap/round1/maker2zffCmds/"

for i in range(0, numberFiles):
	num = str(i)
	fout = open(stemOfFile + num + "_maker2zff", 'w')
	fout.write("cd " + baseDirectory + stemOfFile + num + backFile + " \n")
	logfile = stemOfFile + num + "_master_datastore_index.log"
	fout.write(maker2zff + options + logfile + " \n")
	cmd1 = "mv genome.ann " + tempDir + stemOfFile + num + ".zff.length50_aed0.25.ann \n"
	cmd2 = "mv genome.dna " + tempDir + stemOfFile + num + ".zff.length50_aed0.25.dna \n"
	fout.write(cmd1)
	fout.write(cmd2)
	fout.close()
