inputFile = "c1.out"
inputNames = "stats_clip_HIC_GATC_v2_AGP_Add200.txt"
outFile = "OrganizedClusters.txt"


clusters = 22

f = open(inputNames, 'r')

lstNames = []
sizes = []

for line in f:
        sline = line.split()
        if len(sline) > 0:
                lstNames.append(sline[0])
                sizes.append(int(sline[1]))

f.close()


f = open(inputFile, 'r')

lstCluster = []

counter = 0
for line in f:
	if counter <=1:
		counter+=1
		continue
	lstCluster.append(line)
	counter+=1


f.close()

allClusters = []
allClustersSizes = []

for i in range(0, clusters):
	temp = []
	temp2 = []
	allClusters.append(temp)
	allClustersSizes.append(temp2)

for i in range(0, len(lstCluster)):
	cluster = int(lstCluster[i])
	name = lstNames[i]
	size = sizes[i]

	allClusters[cluster].append(name)
	allClustersSizes[cluster].append(str(size))


fout = open(outFile, 'w')

print(allClustersSizes)

for i in range(0, clusters):
	if i == 0:
		i = 19
		for j in range(0, len(allClusters[i])):
			fout.write(allClusters[i][j] + "\t" + allClustersSizes[i][j] + " \n")
		i= 0 
	elif i == 19:
		i = 0
		for j in range(0, len(allClusters[i])):
			fout.write(allClusters[i][j] + "\t" + allClustersSizes[i][j] + " \n")
		i = 19
	else:
		for j in range(0, len(allClusters[i])):
			fout.write(allClusters[i][j] + "\t" + allClustersSizes[i][j] + " \n")

fout.close()
