fileName = "RestrictionSites_Flanks_GATC.txt"

fin = open(fileName, 'r')


f = [[],[],[]]
r = [[],[],[]]


prevlst = [-1,-1,-1]


scaffoldSizes = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/VisualizeHIC/stats_clip_HIC_v2.txt"

ff = open(scaffoldSizes, 'r')

dicScaf = {}


for line in ff:
	sline = line.split()
	name = sline[0][1:]
	dicScaf[name] = int(sline[1])
ff.close()

scaf = ""
count = 0
for line in fin:
	sline = line.split()
	if scaf != sline[0]:
		if count != 0:
			if count > 0:
				r[0].append(dicScaf[scaf] - int(prevlst[2]))
			if count > 1:
				r[1].append(dicScaf[scaf] - int(prevlst[1]))
			if count > 2:
				r[2].append(dicScaf[scaf] - int(prevlst[0]))
			

		count = 0
		prevlst = [-1,-1,-1]

	scaf = sline[0]

	if count == 0:
		f[0].append(int(sline[1]))
	if count == 1:
		f[1].append(int(sline[1]))
	if count == 2:
		f[2].append(int(sline[1]))

	prevlst[0] = prevlst[1]
	prevlst[1] = prevlst[2]
	prevlst[2] = sline[1]

	count+=1

fin.close()


#print(f)

#print(r)



import matplotlib.pyplot as plt


fig, axes = plt.subplots(3)

axes[0].hist(f[0], bins = 200, label = "site 1")
axes[1].hist(f[1], bins = 200, label = "site 2")
axes[2].hist(f[2], bins = 200, label = "site 3")
axes[0].set_title("First Three RestrictionSites")
axes[0].set_xlim([0,10000])
axes[1].set_xlim([0,10000])
axes[2].set_xlim([0,10000])

axes[0].set_ylim([0,1200])
axes[1].set_ylim([0,1200])
axes[2].set_ylim([0,1200])

plt.savefig("FirstThreeRestrictionSites_GATC.png")

fig, axes = plt.subplots(3)

axes[0].hist(r[0], bins = 200, label = "site n-1")
axes[1].hist(r[1], bins = 200, label = "site n-2")
axes[2].hist(r[2], bins = 200, label = "site n-3")
axes[0].set_title("Last Three RestrictionSites")
axes[0].set_xlim([0,10000])
axes[1].set_xlim([0,10000])
axes[2].set_xlim([0,10000])

axes[0].set_ylim([0,1200])
axes[1].set_ylim([0,1200])
axes[2].set_ylim([0,1200])

plt.savefig("LastThreeRestrictionSites_GATC.png")


print(len(f[0]))
print(len(f[1]))
print(len(f[2]))

print(len(r[0]))
print(len(r[1]))
print(len(r[2]))



