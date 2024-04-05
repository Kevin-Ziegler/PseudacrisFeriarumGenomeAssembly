inputFile = "scaffold_1%7Carrow.gff"

f = open(inputFile, 'r')

listSource = []
listType = []

for line in f:
	sline = line.split()
	if len(sline) > 3:
		source = sline[1]
		type = sline[2]
		if (source in listSource) == False:
			listSource.append(source)
		if (type in listType) == False:
			listType.append(type)
f.close()

#print(listSource)
#print(listType)

#['.', 'maker', 'repeat_gff:repeatmasker', 'blastn', 'est2genome', 'blastx', 'protein2genome']
#['contig', 'gene', 'mRNA', 'exon', 'five_prime_UTR', 'CDS', 'three_prime_UTR', 'match', 'match_part', 'expressed_sequence_match', 'protein_match']



def divideOnField(fileName, field, index, outputFileName):

	f = open(fileName, 'r')

	fout = open(outputFileName, 'w')

	lstField =[]


	for line in f:
		sline = line.split()
		if len(sline) > 3:
			temp_field = sline[index]
			if temp_field == field:
				fout.write(line)
	f.close()
	fout.close()


#divideOnField(inputFile, "maker", 1, "maker.gff")

for i in range(1, len(listSource)):
	print(i)
	divideOnField(inputFile, listSource[i], 1, listSource[i] + ".gff")


