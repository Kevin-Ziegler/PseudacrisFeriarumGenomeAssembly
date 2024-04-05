statsFile = "stats_polished.txt"

f = open(statsFile, 'r')

dict = {}

for line in f:
	sline = line.split()
	name = sline[0][1:]
	length = int(sline[1])
	dict[name] = length

f.close()

#print(dict)



missingCores = [43,51,52,53,54,56,57,58,59]

missingScaffolds = []


realSize = []


for i in range(0, len(missingCores)):
	temp = []
	missingScaffolds.append(temp)
	realSize.append(0)


dataDirc = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/Data/SplitFasta/"


count = 0
for item in missingCores:
	f = open(dataDirc + "scaffolds_v2_GATC_Arrow_2_split" + str(item) + ".fasta", 'r')
	templen = 0
	for line in f:
		if ">" in line:
			sline = line.split()
			templen = templen + dict[sline[0][1:]]
			missingScaffolds[count].append(sline[0][1:])
		else:
			pass
	f.close()
	#completedlen = coreList[item]
	#print(item, completedlen, templen)
	realSize[count] = templen
	count+=1





listLogFiles = "listLogFiles.txt"

fLog = open(listLogFiles, 'r')

totalProgress =0


core =0
coreList = []

for i in range(0, 60):
	coreList.append(0)


for line in fLog:
	logFile = line[:-1]
	ftemp = open(logFile, 'r')
	coreProgress = 0
	temp = ""
	for i in range(0, len(logFile)):
		temp = logFile[i:i+5]
		if temp == "split":
			core = logFile[i+5:i+7]
			if core[1] == ".":
				core = core[0]
			break


	core = int(core)
	#print(core)

	for line2 in ftemp:
		sline = line2.split()
		name = sline[0]
		status = sline[2]
		if status == "FINISHED":
			length = dict[name]
			coreProgress+=length
			if core in missingCores:
				index = 0
				for i in range(0, len(missingCores)):
					if core == missingCores[i]:
						index = i

				if name in missingScaffolds[index]:
					pass
				else:
					print("Name not in split fasta file")
					print(core)
					print(name)
					print(index)
	#print(core, coreProgress)
	ftemp.close()
	totalProgress+=coreProgress
	coreList[core] = coreProgress

	if core in missingCores:
		index = 0
		for i in range(0, len(missingCores)):
			if core == missingCores[i]:
				index = i

		print("Core:", core)
		print("Progress:" , coreProgress)
		print("RealSize:", realSize[index])

fLog.close()
print("Total:", totalProgress)

