import pickle
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy as np

dictionaryFile = "CHI_purgedups_Trimmed_Connections_Locations.pickle"
contigsFile = "RepurgedContigLengths_3_29_2024.txt"
chicDict = {}
fileOut = "MyChicagoConnections.txt"

fout = open(fileOut, 'w')

minAreaRatio = 0.1
maxLength = 100
distanceAllowed = 40000



with open(dictionaryFile, "rb") as file:
	chiDict = pickle.load(file)



print(chiDict["tig00058886_1_tig00002749_1"])

contigsList = []
contigLengthDict = {}
f = open(contigsFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 1:
		continue

	contigsList.append(sline[2])
	contigLengthDict[sline[2]] = int(sline[4])
f.close()



counter = 0
totalNumConnections = 0
blacklist = {}


for item in contigsList:
	#print("For Contig:" + item)
	if counter % 10000 == 0:
		print(counter)
		fout.flush()
	counter +=1
	temp = []


	for item2 in contigsList:
		temp2 = []
		string = item+"_"+item2
		if string in chiDict:
			temp2.append(item2)
			#temp2.append(len(chiDict[string]))
			#hull = ConvexHull(chiDict[string])
			#print(hull.volume)
			#print(hull.area)
			#print(chiDict[string])
			#temp2.append(hull.volume/1600000000.0)
			#numConnections = len(chiDict[string])

			if len(chiDict[string]) > maxLength:
				continue

			x = [item[0] for item in chiDict[string]]
			y = [item[1] for item in chiDict[string]]
			xmean = np.mean(x)
			ymean = np.mean(y)
			filterRangex = 0
			filterRangey = 0
			#print(item2)
			#print("Means")
			#print(xmean, ymean)

			tempx = sorted(x)
			tempy = sorted(y)
			medianx = tempx[int(len(tempx)/2)]
			mediany = tempy[int(len(tempy)/2)]
			orientationContig1 = ""
			orientationContig2 = ""

			distanceFromMedianToEndx = contigLengthDict[item] - medianx
			distanceFromMedianToEndy = contigLengthDict[item2] - mediany


			if medianx < distanceFromMedianToEndx:
				filterRangex = distanceAllowed
				orientationContig1 = "L"
			else:
				filterRangex = contigLengthDict[item] - distanceAllowed
				orientationContig1 = "R"

			if mediany < distanceFromMedianToEndy:
				filterRangey = distanceAllowed
				orientationContig2 = "L"
			else:
				filterRangey = contigLengthDict[item2] - distanceAllowed
				orientationContig2 = "R"

			#print("filter ranges")
			#print(filterRangex, filterRangey)
			newlst = []
			for i in range(0, len(chiDict[string])):
				if filterRangex == distanceAllowed:
					if chiDict[string][i][0] > filterRangex:
						continue
				else:
					if chiDict[string][i][0] < filterRangex:
						continue
				if filterRangey == distanceAllowed:
					if chiDict[string][i][1] > filterRangey:
						continue
				else:
					if chiDict[string][i][1] < filterRangey:
						continue

				newlst.append([chiDict[string][i][0], chiDict[string][i][1]])
				#newy.append(chiDict[string][i][1])
			#print("old then new")
			#print(chiDict[string])
			#print(newlst)

			if newlst == []:
				continue
			if len(newlst) < 5:
				continue
			hull = ConvexHull(newlst)
			numConnections = len(newlst)
			temp2.append(numConnections)
			areaRatio = hull.volume/1600000000.0
			temp2.append(areaRatio)
			temp2.append(orientationContig1)
			temp2.append(orientationContig2)

			if areaRatio < minAreaRatio:
				continue
			#if areaRatio >= minAreaRatio:
			#	continue
			#if numConnections > maxLength:
			#	continue
			temp.append(temp2)

	if temp != []:
		if len(temp) > 2:
			blacklist[item] = 1
			continue
		else:
			#print("For Contig:" + item + " \n")
			#print(temp)
			totalNumConnections = totalNumConnections + len(temp)
			fout.write("For Contig: " + item + " \n")
			for item2 in temp:
				for item3 in item2:
					fout.write(str(item3) + " ")
			fout.write("\n")
fout.close()
print(totalNumConnections)



with open("ChicagoBlackListContigs.pickle", "wb") as file:
	pickle.dump(blacklist, file)
