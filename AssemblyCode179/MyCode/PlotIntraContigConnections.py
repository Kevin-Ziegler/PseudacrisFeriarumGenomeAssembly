import numpy as np

fileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Misc/FilteredHICData"
#fileName = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Misc/FilteredCHIData"


f = open(fileName, 'r')


line = f.readline()
line = f.readline()
line = f.readline()

line = f.readline()


lstLengths = []
sline = line.split(',')

print(sline[0])
print(sline[1])
print(sline[2])


print("Length of sline")
print(len(sline))
print(sline[len(sline)-1])


sline[0] = sline[0][1:]
sline[len(sline)-1] = sline[len(sline)-1][:-2]



print(sline[0])
print(sline[len(sline)-1])

counter = 0 
above10k = 0
for item in sline:
	#lstLengths.append(int(item))
	if(int(item) > 1):
		counter+=1
		lstLengths.append(int(item))
	if counter % 100000 == 0:
		print(counter)

	if counter > 2000000:
		break


print(counter)

above20k = 0
above30k = 0
above40k= 0
above50k = 0
above60k = 0
for item in lstLengths:
	if item >= 10000:
		above10k+=1
	if item >= 20000:
		above20k+=1
	if item >= 30000:
		above30k+=1
	if item >= 40000:
		above40k+=1
	if item >= 50000:
		above50k+=1
	if item >= 60000:
		above60k+=1

print("Above 10k: " + str(above10k))
print("Above 20k: " + str(above20k))
print("Above 30k: " + str(above30k))
print("Above 40k: " + str(above40k))
print("Above 50k: " + str(above50k))
print("Above 60k: " + str(above60k))

import matplotlib.pyplot as plt

bin_range = range(min(lstLengths,), max(lstLengths,) + 10000, 10000)

plt.hist(lstLengths, log = True, bins=bin_range)
plt.show()
#plt.xlim([0,50000])
#plt.savefig("IntraCHILengths_2.png")


