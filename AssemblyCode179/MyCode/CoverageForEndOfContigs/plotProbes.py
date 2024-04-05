import matplotlib.pyplot as plt

inputFile = "TestProbe.txt"

f = open(inputFile)


contigName = ""
counter =0

listForwardProbe1 = []
for line in f:

		contigName = line[:-1]
		print(contigName)
		line = f.readline()
		begin = line.split()
		#line = f.readline()
		#end = line.split()
		line = f.readline()
		forwardProbe = line.split()


		forwardProbe = [float(x) for x in forwardProbe]
		beginfloat = [float(x) for x in begin]
		#endfloat = [float(x) for x in end]
		x = list(range(0, len(beginfloat)))

		#print(x)
		#print(beginfloat)
		print(forwardProbe)
		print(type(x[0]))
		print(type(beginfloat[0]))

		#forwardProbeCov = [
		print(forwardProbe[0])
		print(beginfloat[1])
		forwardProbeCov = []
		forwardProbeCov.append(100)
		forwardProbeCov.append(100)

		plt.figure()
		plt.plot(x, beginfloat, label = "Forward")
		plt.plot(forwardProbe, forwardProbeCov, label= "Probe")
		#plt.title(contigName + " Forward")
		#plt.savefig("Examples/Length_1000/" + contigName+"Forward.png")
		#plt.plot(x, endfloat, label = "End")
		#plt.title(contigName + " End")
		plt.legend()
		plt.yscale('log')
		plt.savefig("Examples/Probes_v1/" + contigName+".png")
		print(counter)
		counter+=1
		listForwardProbe1.append(forwardProbe[0])
		if counter == 153:
		#if counter == 10:
			break


plt.figure()
plt.hist(listForwardProbe1)
plt.title("Histogram of Probe Locations")
plt.savefig("HistogramProbes.png")
print(listForwardProbe1)
f.close()

