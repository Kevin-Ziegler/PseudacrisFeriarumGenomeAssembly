#Creates a histogram of the number of PB reads per Single Copy Kmer
import numpy as np
import matplotlib.pyplot as plt


#inputKmerPBFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/WholeGenomeHiC_Connections_July_31/outputPB_Full.txt"
#inputKmerPBFile = "outputClusters.txt"
inputKmerPBFile = "/pool/KevinChorusFrogGenomeAssembly/Examples/TestDifferentSCKmerThresholds/FullRun/ClusterRun1.txt"

#output_Histogram = "output_Histogram_KmerPB.pdf"
output_Histogram = "output_Histogram_PreCluster.png"


f = open(inputKmerPBFile, 'r')

lstSizes = []

counter = 0

for line in f:
	#print(line)
	line = f.readline()
	if(counter % 1000000 == 0):
		print(counter)
	sline = line.split()
	lstSizes.append(len(sline))
	counter+=1

#for i in range(0,10000):
#	print(lstSizes[i])

his = plt.hist(lstSizes, bins=[1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51])
#his = plt.hist(lstSizes)
#plt.plot(lstSizes)

plt.savefig(output_Histogram)
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

Nmaxelements(lstSizes, 100)

maxCov = 20
counter = 0
for i in range(0, len(lstSizes)):
	if(lstSizes[i] >= maxCov):
		counter+=1
print(counter)

f.close()
