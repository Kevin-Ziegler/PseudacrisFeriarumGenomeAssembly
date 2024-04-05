
import matplotlib.pyplot as plt

inputFile = "/KevinExternalDriveChorusFrogGenomeAssembly/repeat_lib.fasta"

f = open(inputFile, 'r')

lstLength = []
lstCov = []

for line in f:
	if line[0] != ">":
		continue
	sline = line.split("_")
	#print(sline)
	length = float(sline[3])
	cov = sline[5]
	cov = float(cov[:-1])
	lstLength.append(length)
	lstCov.append(lstCov)
	

f.close()

print("Done")

plt.plot(lstLength, lstCov)
plt.title("Length vs Coverage")
plt.savefig("RepARKLengthvsCov.png")
plt.show()

fout = open("RepARKOutput.txt", 'w')

for i in range(0, len(lstLength)):
	fout.write(str(lstLength[i]) +  " " + str(lstCov[i]) + " \n")

fout.close()
