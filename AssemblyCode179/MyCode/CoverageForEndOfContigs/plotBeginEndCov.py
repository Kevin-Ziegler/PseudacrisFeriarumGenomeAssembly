import matplotlib.pyplot as plt

inputFile = "CoverageOf_Beg_End_Contigs.txt"

f = open(inputFile)


contigName = ""
counter =0
for line in f:

		contigName = line[:-1]
		print(contigName)
		line = f.readline()
		begin = line.split()
		line = f.readline()
		end = line.split()

		beginfloat = [float(x) for x in begin]
		endfloat = [float(x) for x in end]
		x = list(range(0, len(endfloat)))

		print(x)
		print(beginfloat)

		print(type(x[0]))
		print(type(beginfloat[0]))


		plt.figure()
		plt.plot(x, beginfloat, label = "Forward")
		#plt.title(contigName + " Forward")
		#plt.savefig("Examples/Length_1000/" + contigName+"Forward.png")
		plt.plot(x, endfloat, label = "End")
		plt.title(contigName + " End")
		plt.legend()
		plt.yscale('log')
		plt.savefig("Examples/Length_1000_Log/" + contigName+".png")
		print(counter)
		counter+=1


f.close()

