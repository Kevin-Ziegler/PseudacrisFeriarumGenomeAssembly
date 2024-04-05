import matplotlib.pyplot as plt

file = "AEDstats.txt"

f = open(file, 'r')

lstAED = []
lstPercentGenes = []

count = 0
for line in f:
	if count == 0:
		count+=1
	else:
		sline = line.split()
		print(sline)
		if len(sline) < 2:
			continue
		lstAED.append(float(sline[0]))
		lstPercentGenes.append(float(sline[1]))
		count+=1
f.close()

print(lstAED)
print(lstPercentGenes)

plt.plot(lstAED, lstPercentGenes)
plt.show()
