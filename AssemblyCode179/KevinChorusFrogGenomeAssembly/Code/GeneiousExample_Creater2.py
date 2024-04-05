FastaFile1 = "/pool/PacBioAssembly/CCS/ccs1.fasta"
FastaFile2 = "/pool/PacBioAssembly/CCS/ccs2.fasta"

#KmerFile_WithPBLineNumbers = "/pool/KevinChorusFrogGenomeAssembly/Examples/WholeGenomeHiC_Connections_July_31/outputPB_Full.txt"
KmerFile_WithPBLineNumbers = "/pool/KevinChorusFrogGenomeAssembly/Code/outputClusters.txt"
outputGeneiousFasta = "/pool/KevinChorusFrogGenomeAssembly/Examples/Misc/Geneious_PreCluster"

numKmersToTake = 100
linesInFastaFile1 = 3267342

inputKmer = open(KmerFile_WithPBLineNumbers, 'r')



def getLineNumber(file1, file2, lineNumber, linesInFile1):
        lineNumber = lineNumber*2+1
	
        if lineNumber <= linesInFile1:
                f = open(file1, 'r')
        else:
                f = open(file2, 'r')
                lineNumber = lineNumber - linesInFile1

        lineNum = 0
        for line in f:
                if lineNum == lineNumber:
                        return line
                lineNum+=1

        return "-1"
kmerLine = inputKmer.readline()
kmerLine = inputKmer.readline()



for i in range(0, numKmersToTake):
	print(i)
	outputG = open(outputGeneiousFasta + str(i) + ".fasta", 'w')
	kmerLine = inputKmer.readline()
	kmerLine = inputKmer.readline()
	sline = kmerLine.split()
	#kmer = sline[0]
	lstPBIds = []
	#outputG.write(">" + str(i)+ " \n");
	#outputG.write(kmer + " \n")


	for j in range(0, len(sline)):
		lstPBIds.append(int(sline[j]))

	
	for j in range(0, len(lstPBIds)):
		#print(j)
		tempLine = getLineNumber(FastaFile1, FastaFile2, lstPBIds[j], linesInFastaFile1)
		outputG.write(">" + str(lstPBIds[j]) + " \n")
		outputG.write(tempLine)

	outputG.close()
inputKmer.close()				


