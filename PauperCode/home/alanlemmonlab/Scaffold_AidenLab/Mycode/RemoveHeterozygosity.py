import matplotlib.pyplot as plt
import math
import os

import numpy as np

def linear_least_squares(x, y):
    """
    Perform linear least squares fitting for a line y = mx + b.
    
    Parameters:
        x (array-like): Array of x coordinates.
        y (array-like): Array of y coordinates.
        
    Returns:
        (float, float): Tuple containing the slope (m) and intercept (b) of the fitted line.
    """
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    # Compute the slope (m) and intercept (b) using the formulas for linear regression
    m = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    b = y_mean - m * x_mean
    
    return m, b

"""
# Example usage:
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 4, 5, 6])

m, b = linear_least_squares(x, y)
print("Slope (m):\t", m)
print("Intercept (b):\t", b)
"""
def filterCloseToLine(m,b, xpoints, ypoints, distanceFromLine):
	newx = []
	newy = []
	for i in range(0, len(xpoints)):
		yline = m*xpoints[i]+b
		if abs(yline-ypoints[i]) < distanceFromLine:
			newx.append(xpoints[i])
			newy.append(ypoints[i])
	return newx, newy


def distanceEuc(x,y,x2,y2):
	return math.sqrt((x-x2)**2 + (y-y2)**2)


def densityFilter(x,y, numberRequiredPoints, distance):
	keepx = []
	keepy = []
	for i in range(0, len(x)):

		numpointsInRange = 0
		for j in range(0, len(x)):
			if distanceEuc(x[i], y[i], x[j], y[j]) < distance:
				numpointsInRange+=1
		if numpointsInRange >= numberRequiredPoints:
			keepx.append(x[i])
			keepy.append(y[i])
	return keepx, keepy


def readFileCoords(inputFile):


	f = open(inputFile, 'r')

	x = []
	y = []

	for line in f:
		sline = line.split()
		if len(sline) > 1:
			x.append(int(sline[0]))
			y.append(int(sline[1]))

	f.close()
	return x, y

#tig00000036_1_tig00057304_1Connections.txt
def parseContigNames(fileName):
	contig1 = fileName[:13]
	contig2 = fileName[14:27]

	return contig1,contig2

def ensureLinkage(x,y, maxDistanceBetweenGaps):
	startIndex = 0
	stopIndex = 0


	for i in range(0, len(x)):
		if x[startIndex] > x[i]:
			startIndex = i
		if x[stopIndex] < x[i]:
			stopIndex = i

	lstReachable = []
	flagReachable = 0
	while 1==1:
		print(x[startIndex], x[stopIndex])
		for i in range(0, len(x)):
			eucDist = distanceEuc(x[startIndex], y[startIndex], x[i], y[i])
			if eucDist <= maxDistanceBetweenGaps and x[i] > x[startIndex]:
				if x[stopIndex] == x[i] and y[stopIndex] == y[i]:
					flagReachable = 1
					break

				lstReachable.append(i)

		if len(lstReachable) == 0 or flagReachable == 1:
			break

		maxx = lstReachable[0]
		for i in range(0, len(lstReachable)):
			if x[lstReachable[i]] > x[maxx]:
				maxx = lstReachable[i]
		startIndex = maxx
		lstReachable = []

	return flagReachable


if __name__ == "__main__":

	inputDir = "/home/alanlemmonlab/Scaffold_AidenLab/Mycode/XYCoords2/"
	outputFile = "ListofRegionsToRemove.txt"


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

	for line in fl:
		sline = line.split()
		contigLengths[sline[0][1:]] = int(sline[2])
	fl.close()






	fout = open(outputFile, 'w')

	files = os.listdir(inputDir)




	for i in range(0, len(files)):
		x,y = readFileCoords(inputDir + files[i])
		newx, newy = densityFilter(x,y, densityRequired, densityRange)
		linex = 0
		liney = 0

		if len(newx) >= 2:
			m, b = linear_least_squares(newx, newy)
			if abs(m) > slopeMaxRequired or abs(m) < slopeMinRequired:
				pass
			else:
				linex, liney = filterCloseToLine(m,b, newx, newy, distanceToLineRequired)
				if len(linex) > 1:
					linkage = ensureLinkage(linex, liney, maxDistanceBetweenGaps)
					if linkage == 0:
						linex = 0
						liney = 0

		print(files[i])
		fout.write(files[i] + " \n")
		if linex != 0 and len(linex) >= 2:
			#print(min(linex), max(linex))
			#print(min(liney), max(liney))
			contig1, contig2 = parseContigNames(files[i])
			lenContig1 = contigLengths[contig1]
			lenContig2 = contigLengths[contig2]
			smallerContig = ""
			smallerLen = ""
			removeStart = ""
			removeStop = ""

			if lenContig1 < lenContig2:
				smallerContig = contig1
				smallerLen = lenContig1
				removeStart = min(linex)
				removeStop = max(linex)
			else:
				smallerContig = contig2
				smallerLen = lenContig2
				removeStart = min(liney)
				removeStop = max(liney)


			fout.write(smallerContig + " Length: " + str(smallerLen) + " \n")
			difference = removeStop - removeStart
			percentToRemove = difference/smallerLen
			leftRemain = removeStart
			rightRemain = smallerLen-removeStop

			print(lenContig1)
			print(lenContig2)

			print(smallerLen)
			print(removeStart)
			print(removeStop)



			if percentToRemove <= percentMin:
				fout.write("nothing \n")
			elif percentToRemove >= percentMax:
				fout.write("0 " + str(smallerLen) + " \n")
			elif leftRemain <= fragmentSizeToRemove and rightRemain <= fragmentSizeToRemove:
				fout.write("0 " + str(smallerLen) + " \n")
			elif leftRemain <= fragmentSizeToRemove:
				removeStart = 0
				difference = removeStop - removeStart
				percentToRemove = difference/smallerLen
				if percentToRemove >= percentMax:
                                	fout.write("0 " + str(smallerLen) + " \n")
				else:
					fout.write("0 " +str(removeStop) + " \n")
			elif rightRemain <= fragmentSizeToRemove:
				removeStop = smallerLen
				difference = removeStop - removeStart
				percentToRemove = difference/smallerLen
				if percentToRemove >= percentMax:
					fout.write("0 " + str(smallerLen) + " \n")
				else:
					fout.write(str(removeStart) + " " + str(smallerLen) + " \n")
			else:
				fout.write(str(removeStart) + " " + str(removeStop) + " \n")
			#fout.write(str(min(linex)) + " " +  str(max(linex)) + " \n")
			#fout.write(str(min(liney)) + " " + str(max(liney)) + " \n")

		else:
			#print("nothing")
			#print("nothing")
			fout.write("nothing \n")
			fout.write("nothing \n")

		fout.flush()
	fout.close()
