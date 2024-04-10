def extract_sequence_from_fasta(file_path, sequence_name):
    """
    Extract a sequence from a FASTA file based on its name/identifier.

    Args:
    file_path (str): Path to the FASTA file.
    sequence_name (str): Name or identifier of the sequence to extract.

    Returns:
    str or None: The sequence if found, or None if the sequence is not in the file.
    """
    sequence = ""
    found = False

    try:
        with open(file_path, "r") as fasta_file:
            current_sequence = ""
            for line in fasta_file:
                line = line.strip()
                if line.startswith(">"):
                    # Check if this is the desired sequence
                    #print(sequence_name)
                    #print(current_sequence)
                    if found == True:
                        break
                    current_sequence = line.split()
                    if len(current_sequence) > 0:
                        current_sequence = current_sequence[0]
                        current_sequence = current_sequence[1:]
                    #print(sequence_name)
                    #print(current_sequence)
                    if current_sequence == sequence_name:
                        found = True
                        continue
                    #current_sequence = line[1:]  # Remove the ">" character
                else:
                    if current_sequence == sequence_name:
                        sequence += line
            # Check if the last sequence in the file is the desired sequence
            if current_sequence == sequence_name:
                found = True
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    if found:
        return sequence
    else:
        return None


def extractQueryFromBlast(fileName, query):
	f = open(fileName, 'r')

	flag_in_query = 0
	qlength = 0
	extractionName = []
	extractionSequence = []
	tempAlign = ""
	first = 0

	for line in f:
		sline = line.split()
		if len(sline) < 1:
			continue

		if sline[0] == "Query=":
			if sline[1] == query:
				flag_in_query = 1
				f.readline()
				temp = f.readline()
				qlength = int(temp[7:])
				continue

		if flag_in_query == 1:
			if len(sline[0]) > 1:
				if sline[0][0] == ">":
					extractionName.append(sline[0][1:])
					if first != 0:
						extractionSequence.append(tempAlign)
					tempAlign = ["-"]*qlength
					first=1

			if sline[0] == "Query":
				start = int(sline[1])
				stop = int(sline[3])
				f.readline()
				line = f.readline()
				sline = line.split()
				seq = sline[2]
				#tempAlign[start-1:stop-1] = seq
				counter = 0
				for i in range(start-1, stop-1):
					tempAlign[i] = seq[counter]
					counter+=1

			if sline[0] == "Effective":
				extractionSequence.append(tempAlign)
				break

	return [extractionName, extractionSequence]

# Example usage:
fasta_file_path = "your_fasta_file.fasta"
sequence_name = "Sequence_1"  # Replace with the name/identifier of the sequence you want to extract
sequence = extract_sequence_from_fasta(fasta_file_path, sequence_name)

if sequence is not None:
    print(f"Sequence '{sequence_name}':\n{sequence}")
else:
    print(f"Sequence '{sequence_name}' not found in the file.")



fileNameTranscripts = "GabaTranscriptNames"
referenceFileName = "/home/alanlemmonlab/NeuronProject/Data/PferAssemblies/Trinity.fasta"
outdirc = "/home/alanlemmonlab/NeuronProject/Results/TestGaba/"
lstBlastResults = ["results.txt", "resultsXenTrop.txt", "resultsHourGlass.txt"]
lstNames = ["Pfer_Genome", "XenTrop_Genome", "HourGlass_Genome"]


f = open(fileNameTranscripts, 'r')

lstTranscripts = []

for line in f:
	lstTranscripts.append(line[:-1])

print(lstTranscripts)


for i in range(0, len(lstTranscripts)):
	refSeq = extract_sequence_from_fasta(referenceFileName, lstTranscripts[i])
	if refSeq == None:
		print("Failed to find ref transcript: " + lstTranscripts[i])
		continue

	outfile = open(outdirc + lstTranscripts[i] + ".fasta", 'w')
	outfile.write(">Pfer_Transcript_" + lstTranscripts[i] + " \n")
	outfile.write(refSeq + " \n")

	for j in range(0, len(lstBlastResults)):
		ans = extractQueryFromBlast(lstBlastResults[j], lstTranscripts[i])
		for k in range(0, len(ans[0])):
			outfile.write(">" + lstNames[j] + "_" + ans[0][k] + " \n")
			temp = ""
			for item in ans[1][k]:
				temp = temp + item
			outfile.write(temp + " \n")



outfile.close()
