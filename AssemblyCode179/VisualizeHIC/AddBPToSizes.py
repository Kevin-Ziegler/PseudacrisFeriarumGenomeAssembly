filename = "Try2GATC/stats_clip_HIC_GATC_v2_AGP.txt"
out = "Try2GATC/stats_clip_HIC_GATC_v2_AGP_Add200.txt"

f = open(filename, 'r')
fout  = open(out, 'w')

basesToAdd = 200

for line in f:
	#line = line[1:]
	sline = line.split()
	temp = int(sline[1])
	temp = temp + basesToAdd
	fout.write(sline[0] + "\t" + str(temp) + " \n")

fout.close()
f.close()
