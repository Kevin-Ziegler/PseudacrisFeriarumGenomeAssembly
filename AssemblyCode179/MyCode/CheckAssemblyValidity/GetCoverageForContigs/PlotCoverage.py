import matplotlib.pyplot as plt
import os

#inputContigs = "ContigHeaders.txt"

#datadir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/CoverageContigs/"
#dataout = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/PlotsContigCoverage/"

#datadir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/AnuranDups/"
#dataout = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/AnuranDups/Plots/"

datadir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/ExampleMisjoinCoverage/"
dataout = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/MyCode/CheckAssemblyValidity/GetCoverageForContigs/ExampleMisjoinCoverage/Plots/"


files = os.listdir(datadir)

"""
f = open(inputContigs, 'r')

lstContigs = []

for line in f:
	lstContigs.append(
"""


lstcontigs = []

for item in files:
	if "_Coverage.txt" in item:
		lstcontigs.append(item)

print(lstcontigs)
"""
lstcontigs = ["tig00000006_1",
"tig00000023_1",
"tig00000036_1",
"tig00000042_1",
"tig00000043_1",
"tig00000048_1",
"tig00000050_1",
"tig00000060_1",
"tig00000086_1",
"tig00000089_1",
"tig00000124_1",
"tig00000139_1",
"tig00000150_1",
"tig00000158_1",
"tig00000161_1",
"tig00000163_1",
"tig00000169_1",
"tig00000170_1",
"tig00000180_1",
"tig00000198_1",
"tig00000206_1",
"tig00000216_1"]
"""


for item in lstcontigs:
	print(item)

	fpb = open(datadir+item[:-13]+"_PBCoverage.txt", 'r')
	line = fpb.readline()
	pbdata = line.split()
	fpb.close()

	fil = open(datadir+item, 'r')
	line = fil.readline()
	ildata = line.split()
	fil.close()
	print(len(pbdata))
	print(len(ildata))

	for i in range(0, len(pbdata)):
		pbdata[i] = int(pbdata[i])
	for i in range(0, len(ildata)):
		ildata[i] = int(ildata[i])

	plt.figure(figsize=(20, 10))
	plt.plot(pbdata, 'ro' , markersize = .25)
	plt.plot(ildata, 'bo', markersize = .25)
	plt.plot([0,len(pbdata)], [57,57], 'g')
	plt.plot([0,len(pbdata)], [28,28], 'g')
	plt.plot([0,len(ildata)], [100,100], 'k')
	plt.plot([0,len(ildata)], [200,200], 'k')
	plt.yscale('log')
	plt.savefig(dataout + item + ".png")
	plt.show()
	#break
