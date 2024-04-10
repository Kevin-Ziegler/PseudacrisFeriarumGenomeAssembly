print("before import")

import matplotlib.pyplot as plt
import math

import numpy as np
import RemoveHeterozygosity



print("after import")

contigLengths = {}

inputLengthsFile = "ContigLengths.txt"
densityRequired= 25
densityRange = 1000
distanceToLineRequired = 5000
slopeMinRequired = 0.6
slopeMaxRequired = 1.4
fragmentSizeToRemove = 20000
percentMin = 0.10
percentMax = 0.50
maxDistanceBetweenGaps = 25000

fl = open(inputLengthsFile, 'r')

print("getting lengths")


for line in fl:
	sline = line.split()
	contigLengths[sline[0][1:]] = int(sline[2])
fl.close()



inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/XYCoords2/tig00066508_1_tig00066507_1Connections.txt"
#inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/XYCoords2/tig00002156_1_tig00059256_1Connections.txt"
#inputFile = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/XYCoords2/tig00008823_1_tig00061483_1Connections.txt"


print("start read")

x,y = RemoveHeterozygosity.readFileCoords(inputFile)
newx, newy = RemoveHeterozygosity.densityFilter(x,y, densityRequired, densityRange)
linex = 0
liney = 0

m = 0
b = 0
linkage = -1


linex = 0
liney = 0

if len(newx) >= 2:
	m, b = RemoveHeterozygosity.linear_least_squares(newx, newy)
	#print("m", m)
	#print("b", b)
	if abs(m) > slopeMaxRequired or abs(m) < slopeMinRequired:
		pass
	else:
		linex, liney = RemoveHeterozygosity.filterCloseToLine(m,b, newx, newy, distanceToLineRequired)
		linkage = RemoveHeterozygosity.ensureLinkage(linex, liney, maxDistanceBetweenGaps)
		#print("linkage", linkage)


plt.plot(x,y, 'ro')
plt.show()


plt.plot(newx, newy, 'bo')
#plt.show()


#m, b = linear_least_squares(newx, newy)
print("Slope (m):\t", m)
print("Intercept (b):\t", b)
print("linkage", linkage)

min(newx)

c= m*min(newx) + b
c2 = m*max(newx) + b

plt.plot([min(newx), max(newx)], [c,c2], 'k')
plt.show()

#linex, liney = filterCloseToLine(m,b, newx, newy, 5000)

print(linex)
print(liney)

plt.plot(linex, liney, 'go')
c= m*min(linex) + b
c2 = m*max(linex) + b

plt.plot([min(linex), max(linex)], [c,c2], 'k')

plt.show()





