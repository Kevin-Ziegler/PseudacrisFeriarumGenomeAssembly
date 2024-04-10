import pickle
import sys

#tig00021851_1 45 0.10918072593749999 L L tig00067747_1 39 0.1288765540625 L R

inputFile = "MyChicagoConnections.txt"
purgeHeterozygosityFile = "PurgeDoubleListedHeteroztgosityMissed.txt"

ShouldFullyPurgeMissed = []

fpurge = open(purgeHeterozygosityFile, 'r')

for line in fpurge:
	base = line.strip()
	b1 = base+"_1"
	b2= base + "_2"
	ShouldFullyPurgeMissed.append(b1)
	ShouldFullyPurgeMissed.append(b2)
fpurge.close()

print(ShouldFullyPurgeMissed)
#sys.exit()

f = open(inputFile, 'r')

blacklist = {}

with open("ChicagoBlackListContigs.pickle", "rb") as file:
	blacklist = pickle.load(file)

print(blacklist)



myDictLRConnections = {}
ConnectionsUsed = {}
DoubleMapped = {}

for line in f:
	sline = line.split()
	line2 = f.readline()
	sline2 = line2.split()

	if len(sline) < 1 or len(sline2) < 1:
		continue
	contig1 = sline[2]
	contig2 = sline2[0]
	flagpass = 0

	if contig2 in blacklist:
		flagpass =1

	#print(contig1)
	if contig1 in ShouldFullyPurgeMissed:
		flagpass = 1
		print("Inmissed purge")
		print(contig1)

	if contig2 in ShouldFullyPurgeMissed:
		print("In missed purgge")
		print(contig2)
		flagpass = 1

	if flagpass == 0:

		contig1LR = sline2[3]
		contig2LR = sline2[4]




		if contig1 in myDictLRConnections:
			temp = myDictLRConnections[contig1]
			if contig1LR == "L":
				if temp[0] != contig2 and temp[0] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(contig1LR, contig2LR)
					print(line)
					print(line2)
					DoubleMapped[contig1+"_"+contig1LR] = 1
					DoubleMapped[contig2+"_"+contig2LR] = 1

				else:
					temp[0] = contig2
			else:
				if temp[1] != contig2 and temp[1] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(contig1LR, contig2LR)
					print(line)
					print(line2)
					DoubleMapped[contig1+"_"+contig1LR] = 1
					DoubleMapped[contig2+"_"+contig2LR] = 1

				else:
					temp[1] = contig2
			myDictLRConnections[contig1] = temp

		else:
			if contig1LR == "L":
				myDictLRConnections[contig1] = [contig2,""]
			if contig1LR == "R":
				myDictLRConnections[contig1] = ["", contig2]


		"""
		if contig2 in myDictLRConnections:
			temp = myDictLRConnections[contig2]
			if contig2LR == "L":
				if temp[0] != contig1 and temp[0] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(line)
					print(line2)
				else:
					temp[0] = contig1
			else:
				if temp[1] != contig1 and temp[1] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(line)
					print(line2)
				else:
					temp[1] = contig1

		else:
			if contig2LR == "L":
				myDictLRConnections[contig2] = [contig1,""]
			if contig2LR == "R":
				myDictLRConnections[contig2] = ["", contig1]


		"""
	if len(sline2) > 5:
		contig2 = sline2[5]
		contig1LR = sline2[8]
		contig2LR = sline2[9]

		if contig2 in blacklist:
			continue
		if contig1 in ShouldFullyPurgeMissed:
			continue

		if contig2 in ShouldFullyPurgeMissed:
			continue

		if contig1 in myDictLRConnections:
			temp = myDictLRConnections[contig1]
			if contig1LR == "L":
				if temp[0] != contig2 and temp[0] != "":
					print("duplicate entry")
					#print(contig1LR, contig2LR)
					print(contig1, contig2)
					print(contig1LR, contig2LR)
					print(line)
					print(line2)
					DoubleMapped[contig1+"_"+contig1LR] = 1
					DoubleMapped[contig2+"_"+contig2LR] = 1

				else:
					temp[0] = contig2
			else:
				if temp[1] != contig2 and temp[1] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(contig1LR, contig2LR)
					print(line)
					print(line2)
					DoubleMapped[contig1+"_"+contig1LR] = 1
					DoubleMapped[contig2+"_"+contig2LR] = 1

				else:
					temp[1] = contig2

			myDictLRConnections[contig1] = temp

		else:
			if contig1LR == "L":
				myDictLRConnections[contig1] = [contig2,""]
			if contig1LR == "R":
				myDictLRConnections[contig1] = ["", contig2]
		"""

		if contig2 in myDictLRConnections:
			temp = myDictLRConnections[contig2]
			if contig2LR == "L":
				if temp[0] != contig1 and temp[0] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(line)
					print(line2)
				else:
					temp[0] = contig1
			else:
				if temp[1] != contig1 and temp[1] != "":
					print("duplicate entry")
					print(contig1, contig2)
					print(line)
					print(line2)
				else:
					temp[1] = contig1

		else:
			if contig2LR == "L":
				myDictLRConnections[contig2] = [contig1,""]
			if contig2LR == "R":
				myDictLRConnections[contig2] = ["", contig1]
		"""


f.close()

#print(DoubleMapped)

#Remove Double maps
for item in DoubleMapped:
	print(item)
	pos = item[-1:]
	contig = item[:-2]
	if pos == "L":
		myDictLRConnections[contig][0] = ""
	if pos == "R":
		myDictLRConnections[contig][1] = ""



#print(myDictLRConnections)
print(len(myDictLRConnections))

scaffoldList = []
scaffoldListDirection = []

usedContig = {}

def getDirection(dict, prev, current, prevdirection):
	prevLocation = ""
	if dict[prev][0] == current:
		prevLocation = "L"
	if dict[prev][1] == current:
		prevLocation = "R"

	currentLocation = ""
	if dict[current][0] == prev:
		currentLocation = "L"
	if dict[current][1] == prev:
		currentLocation = "R"

	flaginvert = 0
	if prevLocation == currentLocation:
		flaginvert = 1
	direction = ""
	if flaginvert == 0:
		direction = prevdirection
	else:
		if prevdirection == "+":
			direction = "-"
		if prevdirection == "-":
			direction = "+"
	#print("In Direction:")
	#print(prev)
	#print(current)
	#print(prevLocation)
	#print(currentLocation)
	#print(prevdirection)
	#print(direction)
	return direction


for item in myDictLRConnections:
	if item in usedContig:
		continue


	usedContig[item] = 1
	left = myDictLRConnections[item][0]
	right = myDictLRConnections[item][1]

	lst = []
	lstDirection = []
	lst.append(item)
	lstDirection.append("+")

	if left != "":
		#lst.insert(0, left)
		previous = item
		previousdirection = "+"
		while 1==1:
			lst.insert(0, left)
			newdirection = getDirection(myDictLRConnections, previous, left, previousdirection)
			lstDirection.insert(0, newdirection)
			previousdirection = newdirection
			previous = left
			#newitem = myDictLRConnections[left]
			usedContig[left] = 1
			newleft = myDictLRConnections[left][0]
			newright = myDictLRConnections[left][1]
			if ((newleft in lst) == False) and newleft != "":
				left = newleft
			elif ((newright in lst) == False) and newright != "":
				left = newright
			else:
				break

	if right != "":
		#lst.insert(0, left)
		previous = item
		previousdirection = "+"
		while 1==1:
			print(right)
			lst.append(right)
			newdirection = getDirection(myDictLRConnections, previous, right, previousdirection)
			lstDirection.append(newdirection)
			previousdirection = newdirection
			previous = right

			#newitem = myDictLRConnections[right]
			usedContig[right] = 1
			newleft = myDictLRConnections[right][0]
			newright = myDictLRConnections[right][1]
			if ((newleft in lst) == False) and newleft != "":
				#print("first")
				right = newleft
			elif ((newright in lst) == False) and newright !="":
				#print("second")
				#print(right)
				#print(newright)
				#print(newright != right)
				right = newright
			else:
				break
	#print(lst)
	scaffoldList.append(lst)
	scaffoldListDirection.append(lstDirection)

#print(scaffoldList)
#print(scaffoldListDirection)
dictcounts = {}

totaljoins = 0
for item in scaffoldList:
	#print(len(item))
	totaljoins = totaljoins + len(item)
	if str(len(item)) in dictcounts:
		dictcounts[str(len(item))]+=1
	else:
		dictcounts[str(len(item))] = 1
print(dictcounts)

print(totaljoins)



dictJuiceBoxNamesFile = "JuiceBoxChicagoNames.txt"
names = {}

f = open(dictJuiceBoxNamesFile, 'r')

for line in f:
	sline = line.split()
	if len(sline) < 2:
		continue
	contig = sline[0][1:]
	name = sline[1]
	names[contig] = name
f.close()

fileout = "JuiceBoxMyChicagoScaffolds.assembly"
fout = open(fileout, 'w')

for i in range(0, len(scaffoldList)):
	lst = scaffoldList[i]
	lstdir = scaffoldListDirection[i]
	if len(lst) <= 1:
		continue
	for j in range(0, len(lst)):
		convertedName = names[lst[j]]
		dir = lstdir[j]
		combined = ""
		if dir == "-":
			combined = "-" + convertedName
		else:
			combined = convertedName
		fout.write(combined + " ")
	fout.write("\n")
fout.close()


"""
for i in range(0, len(scaffoldList)):
	lst = scaffoldList[i]
	lstdir = scaffoldListDirection[i]
	if len(lst) <= 1:
		continue
	for j in range(0, len(lst)):
		convertedName = names[lst[j]]
		dir = lstdir[j]
		combined = ""
		if dir == "-":
			combined = "-" + convertedName
		else:
			combined = convertedName
		fout.write(combined + " ")
	fout.write("\n")
fout.close()
"""
