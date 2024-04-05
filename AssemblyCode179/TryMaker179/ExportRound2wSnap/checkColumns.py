inputFile = "scaffolds_v2_GATC_Arrow_2_Full_r2.maker.noseq.gff"
#['3', '.', 'snap_masked', 'maker', 'repeat_gff:repeatmasker', 'protein_gff:protein2genome', 'est_gff:est2genome']

f = open(inputFile, 'r')

col = []

for line in f:
	sline = line.split()
	if len(sline) < 2:
		continue
	if sline[1] in col:
		pass
	else:
		col.append(sline[1])

f.close()

print(col)
