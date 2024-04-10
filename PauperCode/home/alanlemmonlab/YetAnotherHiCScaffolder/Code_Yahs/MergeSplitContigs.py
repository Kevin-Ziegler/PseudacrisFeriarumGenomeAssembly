fileAGP = "/home/alanlemmonlab/HiCData/Scaffolding/ScaffoldingFolder/mapping_pipeline/PurgedChicago_v2_GATC/scaffolds_FINAL.agp"

f = open(fileAGP, 'r')


splitContigs = []
lengths = []

splitContigsDict = {}

for line in f:
	sline = line.split()
	if len(sline) < 5:
		continue
	contig = sline[5]
	length = sline[7]
	
	count_ = 0
	for item in contig:
		if item == "_":
			count_+=1
	if count_ == 2:
		splitContigs.append(contig)
		lengths.append(length)
		splitContigsDict[contig] = length

print(splitContigs)
print(lengths)

f.close()

baseNames = {}



for i in range(0, len(splitContigs)):
	baseName = ""
	for j in range(0, len(splitContigs[i])):
		if splitContigs[i][j] == "_":
			break
		else:
			baseName = baseName + splitContigs[i][j]
	if baseName in baseNames:
		baseNames[baseName] = baseNames[baseName] + 1
	else:
		baseNames[baseName] = 1

print(baseNames)


print(splitContigsDict)


fileBed = "HicToCanu_v2.bed"
fileOut = "HicToCanu_v2_Merged.bed"

f = open(fileBed, 'r')
fout = open(fileOut, 'w')

counter = 0
for line in f:
	if counter % 1000000 == 0:
		print(counter)
	counter+=1

	sline = line.split()
	if len(sline) < 3:
		continue

	name = sline[0]
	start = sline[1]
	end = sline[2]

	if name in splitContigsDict:
		baseName = ""

		for j in range(0, len(name)):
			if name[j] == "_":
				break
			else:
				baseName = baseName + name[j]
		tempLen = splitContigsDict[name]
		lastDigit = name[len(name)-1]
		if lastDigit == "1":
			pass
		if lastDigit == "2":
			start = str(int(start) + int(splitContigsDict[baseName + "_1_1"]))
			end = str(int(end) + int(splitContigsDict[baseName + "_1_1"]))
		name = baseName + "_1"
	fout.write(name + "\t" + start + "\t" + end + "\t" + sline[3] + "\t" + sline[4] + "\t" + sline[5] + " \n")


f.close()
fout.close()



