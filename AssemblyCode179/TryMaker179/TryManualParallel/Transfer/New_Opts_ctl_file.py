import sys

subFasta = sys.argv[1]
ctlFile = sys.argv[2]
outdir = sys.argv[3]

fin = open(ctlFile, 'r')

fout = open(outdir + "maker_opts.ctl", 'w') 

counter = 0
for line in fin:
	if counter == 1:
		fout.write("genome=" + subFasta + " #genome sequence (fasta file or fasta embeded in GFF3 file) \n")
		counter+=1
	else:
		fout.write(line)
		counter+=1
fout.close()
fin.close()
