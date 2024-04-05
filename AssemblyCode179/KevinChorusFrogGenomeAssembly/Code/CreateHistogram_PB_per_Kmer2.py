#Creates a histogram of the number of PB reads per Single Copy Kmer
import numpy as np
import matplotlib.pyplot as plt


#inputKmerPBFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/WholeGenomeHiC_Connections_July_31/outputPB_Full.txt"
inputKmerPBFile = "outputHiC_Connections_Log.txt"
output_Histogram1 = "output_Histogram_HiC_SC.png"
output_Histogram2 = "output_Histogram_HiC_First.png"
output_Histogram3 = "output_Histogram_HiC_Last.png"

def removeUnderScore(x):
	temp = ""
	for i in range(0, len(x)):
		if x[i] != "_":
			temp = temp + x[i]
	return temp

f = open(inputKmerPBFile, 'r')

lstSC = []
lstFirst = []
lstLast = []

counter = 0

for line in f:
	#print(line)
	if(counter % 1000000 == 0):
		print(counter)
	sline = line.split()
	lstSC.append(int(sline[1]))
	pos = sline[2]
	pos = pos.split(",")
	first = pos[0]
	last = pos[len(pos)-1]
	first = removeUnderScore(first)
	last = removeUnderScore(last)

	if last == '':
		last = pos[len(pos)-2]
		last = removeUnderScore(last)
	lstFirst.append(int(first))
	lstLast.append(int(last))
	counter+=1

#for i in range(0,10000):
#	print(lstSizes[i])

#his = plt.hist(lstSC)
#plt.plot(lstSizes)

#plt.savefig(output_Histogram1)
#plt.show()


his = plt.hist(lstFirst)
#plt.plot(lstSizes)

plt.savefig(output_Histogram2)
plt.show()

#his = plt.hist(lstLast)
#plt.plot(lstSizes)

#plt.savefig(output_Histogram3)
#plt.show()

def Nmaxelements(list1, N):
    final_list = []
  
    for i in range(0, N): 
        max1 = 0
          
        for j in range(len(list1)):     
            if list1[j] > max1:
                max1 = list1[j];
                  
        list1.remove(max1);
        final_list.append(max1)
          
    print(final_list)

#Nmaxelements(lstSizes, 100)

maxCov = 20
counter = 0
#for i in range(0, len(lstSizes)):
#	if(lstSizes[i] >= maxCov):
#		counter+=1
#print(counter)

f.close()
