def extract_sequences_from_fasta(file_path, target_individuals):
    """
    Extract sequences for specific individuals from a FASTA file.

    Args:
    file_path (str): Path to the FASTA file.
    target_individuals (list): List of sequence identifiers to extract.

    Returns:
    dict: A dictionary where keys are sequence identifiers and values are the sequences for the target individuals.
    """
    sequences = {}
    current_id = None
    current_sequence = []
    extracting = False

    try:
        with open(file_path, "r") as fasta_file:
            for line in fasta_file:
                line = line.strip()
                if line.startswith(">"):
                    if current_id is not None and extracting:
                        sequences[current_id] = ''.join(current_sequence)
                    current_id = line[1:]  # Remove the ">" character
                    current_id = current_id.split()
                    current_id = current_id[0]
                    current_sequence = []
                    if current_id in target_individuals:
                        extracting = True
                    else:
                        extracting = False
                elif extracting:
                    current_sequence.append(line)
            # Add the last sequence if it's for a target individual
            if current_id is not None and extracting:
                sequences[current_id] = ''.join(current_sequence)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return sequences

# Example usage:
#fasta_file_path = "your_fasta_file.fasta"
#target_individuals = ["Sequence_1", "Sequence_3"]  # List of individuals to extract
#sequence_dict = extract_sequences_from_fasta(fasta_file_path, target_individuals)

# Access individual sequences by their identifiers, e.g., sequence_dict["Sequence_1"]


fileNameToExtract = "GabaTranscriptNames"
TranscriptAssembly = "/pool/Kevin81/NeuronProject/Data/PferAssemblies/Trinity.fasta"
f = open(fileNameToExtract, 'r')
lstTranscriptName = []


for line in f:
	lstTranscriptName.append(line[:-1])

#print(lstTranscriptName)

f.close()


sequence_dict = extract_sequences_from_fasta(TranscriptAssembly, lstTranscriptName)
#print(sequence_dict)

for item in lstTranscriptName:
	#print(">" + item)
	if item in sequence_dict:
		print(">" + item)
		print(sequence_dict[item])
	else:
		#print("Item not Found")
		pass


