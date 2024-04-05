inputF = "scaffolds_HIC_v2_GATC.agp"
outFile = "stats_clip_HIC_GATC_v2_AGP.txt"

f = open(inputF, 'r')
fout = open(outFile, 'w')

counter = 0
scaf = ""
prevline = ""
sline = []
for line in f:
	prevline = sline
	sline = line.split()
	#print(line)
	if len(sline) < 4 or len(prevline) < 4:
		continue
	if sline[3] == "1":
		fout.write(prevline[0] +"\t" + prevline[2] + " \n")

#print(prevline)
#fout.write(prevline[0] +"\t" + prevline[2] + " \n")

fout.close()
f.close()
