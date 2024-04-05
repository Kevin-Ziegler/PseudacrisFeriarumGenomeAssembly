import sys

inputFile = sys.argv[1]


f = open(inputFile, 'r')

countTotal = 0
countSame = 0
countDifferent = 0
DistanceSameList = []

for line in f:
	line2 = f.readline()
	sline = line.split()
	sline2 = line2.split()

	if sline[0] == sline2[0]:
		countSame+=1
		diff = abs(int(sline[1])-int(sline2[1]))
		DistanceSameList.append(diff)
	else:
		countDifferent+=1

countTotal = countSame + countDifferent
print(countDifferent)
print(countSame)
print(countTotal)

print(DistanceSameList)



