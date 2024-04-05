#pferBusco = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/BuscoTransfer_3_7_2024/Pfer_full_table.csv"
pferBusco = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/Busco_v2/run_tetrapoda_odb10/full_table.tsv"
hylasarda = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/BuscoTransfer_3_7_2024/HylaSarda_full_table_converted.csv"
xentrop = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/BuscoTransfer_3_7_2024/XenTrop_full_table_converted.csv"

lstPferD = {}
lstHylaSardaD = {}
lstXenTropD = {}

lstfiles = [pferBusco, hylasarda, xentrop]
lstDict = [lstPferD, lstHylaSardaD, lstXenTropD]

for i in range(0, len(lstfiles)):

	f = open(lstfiles[i], 'r')

	for line in f:
		sline = line.split()
		if sline[1] == "Duplicated":
			if sline[0] in lstDict[i]:
				lstDict[i][sline[0]].append(sline[2])
			else:
				lstDict[i][sline[0]] = [sline[2]]
f.close()

#print(lstPferD)
#print(lstHylaSardaD)
#print(lstXenTropD)

number = 20

PferuniqueDups = 0
PferandAnuranDups = 0

lstPferUniqueDups = []
lstAnuranDups = []

counter = 0
for item in lstPferD:
	print(item)
	counter +=1
	if item in lstHylaSardaD and item in lstXenTropD:
		if PferandAnuranDups < 20:
			lstAnuranDups.append(item)
		PferandAnuranDups+=1
	if ((item in lstHylaSardaD) == False) and ((item in lstXenTropD) == False):
		if PferuniqueDups < 20:
			lstPferUniqueDups.append(item)
		PferuniqueDups+=1
	if PferandAnuranDups >= 20 and PferuniqueDups >= 20:
		print("broke")
		break


print(lstPferUniqueDups)
print(lstAnuranDups)

print("PferDups")
for item in lstPferUniqueDups:
	lst = lstPferD[item]
	print(item)
	for item2 in lst:
		print(item2)

print("Anuran Dups")
for item in lstAnuranDups:
	lst = lstPferD[item]
	print(item)
	for item2 in lst:
		print(item2)
