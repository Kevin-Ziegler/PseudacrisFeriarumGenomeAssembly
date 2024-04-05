file = "ReadsMappedToContigs.txt"

f = open(file ,'r')

total = 0

for line in f:
	sline = line.split()
	temp = int(sline[1])
	total = total + temp

print(total)
