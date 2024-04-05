import sys

subFasta = sys.argv[1]
ctlFile = sys.argv[2]
outdir = sys.argv[3]
stemPrev = sys.argv[4]

round1FilesDirc = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/Transfer/" 


fin = open(ctlFile, 'r')

fout = open(outdir + "maker_opts.ctl", 'w') 

#18 23 29


counter = 0
for line in fin:
	if counter == 1:
		fout.write("genome=" + subFasta + " #genome sequence (fasta file or fasta embeded in GFF3 file) \n")
		counter+=1
	elif counter == 17:
		fout.write("est_gff=" + round1FilesDirc + stemPrev + ".maker.output/" + stemPrev + ".maker." + "est2genome.gff" + " #aligned ESTs or mRNA-seq from an external GFF3 file \n")
		counter+=1
	elif counter == 22:
		fout.write("protein_gff=" + round1FilesDirc + stemPrev + ".maker.output/" + stemPrev + ".maker." + "protein2genome.gff" + " #aligned protein homology evidence from an external GFF3 file \n")
		counter+=1
	elif counter == 28:
		fout.write("rm_gff=" + round1FilesDirc + stemPrev + ".maker.output/" + stemPrev + ".maker." + "repeat.gff" + " #pre-identified repeat elements from an external GFF3 file \n")
		counter+=1
	else:
		fout.write(line)
		counter+=1
fout.close()
fin.close()
