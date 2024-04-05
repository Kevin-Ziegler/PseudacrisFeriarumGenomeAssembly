#inputFile = "align.sam"
#inputFile = "test"
#inputFile = "Combined_2.sam"
inputFile = "t3"

f = open(inputFile, 'r')


lineNum = 0
flagHeaders = 0

def checkOptional(x):
	countColon = 0
	flag = 0
	for i in range(0, len(x)):
		if x[i] == ":":
			countColon+=1
	if countColon == 2 and x[len(x)-1] != ":":
		flag = 1
	return flag


for line in f:
	sline = line.split()
	#print(sline)
	#print(len(sline))

	#break
	if "@" in line:
		if flagHeaders == 1:
			print("Error H " + str(lineNum))
			break

		if "@PG" in line:

			if len(sline) != 13:
				print("Error @PG " + str(lineNum))
				break
		if "@SQ" in line:
			if len(sline) != 3:
				print("Error @SQ " + str(lineNum))
	else:
		flagHeaders = 1
		if len(sline) < 11:
			print("Error N " + str(lineNum))
			break

		if  len(sline) > 11:
			flag2 = 0

			for i in range(11, len(sline)):
				flag = checkOptional(sline[i])
				if  flag == 0:
					flag2 = 1
			if flag2 == 1:
				print("Error Opt " + str(lineNum))
				break
	if lineNum % 1000000 == 0:
		print(lineNum)
	lineNum +=1

f.close()
