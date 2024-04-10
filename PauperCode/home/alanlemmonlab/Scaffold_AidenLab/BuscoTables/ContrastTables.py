inputMM = "table_PurgeMM.tsv"
inputDefault = "table_PurgeDups.tsv"


dictBuscos = {}



f = open(inputDefault, 'r')

f.readline()
f.readline()
f.readline()

for line in f:
	sline = line.split()
	if len(sline) > 1:
		geneId = sline[0]
		status = sline[1]
		contig = ""
		if status != "Missing":
			contig = sline[2]
		dictBuscos[geneId] = [status, contig, 0, 0]

f.close()


f = open(inputMM, 'r')

f.readline()
f.readline()
f.readline()

for line in f:
	sline = line.split()
	if len(sline) > 1:
		geneId = sline[0]
		status = sline[1]
		contig = ""
		if status != "Missing":
			contig = sline[2]
		dictBuscos[geneId][2] = status
		dictBuscos[geneId][3] = contig

f.close()

#print(dictBuscos)

#combos = [["Complete", "Complete"], ["Duplicated", "Complete"], ["Complete", "Duplicated"]]

elements = ["Complete", "Duplicated", "Fragmented", "Missing"]

for item in elements:
	for item2 in elements:
			count = 0
			for item3 in dictBuscos:
				lst = dictBuscos[item3]
				if lst[0] == item and lst[2] == item2:
					count+=1
					if item == "Complete" and item2 == "Missing":
						print(lst[1])
			print(item, item2)
			print(count)
