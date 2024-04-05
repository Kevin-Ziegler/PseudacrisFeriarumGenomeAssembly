cores = 30
numberFiles = 60

stemOfFile = "scaffolds_v2_GATC_Arrow_2_split"
backFile = ".maker.output"
baseDirectory = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/Transfer/"

#maker2zff = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/maker/bin/maker2zff"
#options = " -x 0.25 -l 50 -d "

binMaker = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/maker/bin/"


tempDir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/snap/round1/groupOutput/"

for i in range(0, numberFiles):
	num = str(i)
	fout = open(stemOfFile + num + "_groupOutput", 'w')
	fout.write("cd " + baseDirectory + stemOfFile + num + backFile + " \n")
	logfile = stemOfFile + num + "_master_datastore_index.log"
	cmd1 = binMaker + "gff3_merge -s -d " + logfile + " > " + stemOfFile + num + ".maker.gff \n"
	cmd2 = binMaker + "fasta_merge -d " + logfile + " \n"
	cmd3 = binMaker + "gff3_merge -n -s -d " + logfile + " > " + stemOfFile + num + ".maker.noseq.gff \n"
	
	noseqFile = stemOfFile + num + ".maker.noseq.gff"

	cmd4 = "awk '{ if ($2 == " + '"est2genome"' + ") print $0 }' " + noseqFile + " > " + stemOfFile + num + ".maker.est2genome.gff \n"
	cmd5 = "awk '{ if ($2 == " + '"protein2genome"' + ") print $0 }' " + noseqFile + " > " + stemOfFile + num + ".maker.protein2genome.gff \n"
	cmd6 = "awk '{ if ($2 ~ " + '"repeat"' + ") print $0 }' " + noseqFile + " > " + stemOfFile + num + ".maker.repeat.gff \n"
	fout.write(cmd1)
	fout.write(cmd2)
	fout.write(cmd3)

	fout.write(cmd4)
	fout.write(cmd5)
	fout.write(cmd6)
	fout.close()
