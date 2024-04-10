f = open("temp3", 'r')


lstsame = []
lstdiff = []

for line in f:
	sline = line.split()
	if sline[1] == "tig00010600_1"  and sline[5] == "tig00010600_1":
		lstsame.append(sline[14])
		lstsame.append(sline[15])
	if sline[5] == "tig00010609_1":
		lstdiff.append(sline[14])
		lstdiff.append(sline[15])


counter = 0
for item in lstsame:
	if item in lstdiff:
		print(item)
		counter+=1

print(counter)
