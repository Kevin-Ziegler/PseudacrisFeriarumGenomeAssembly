# Define a function to translate a DNA sequence into amino acids
def translate_dna_to_aa(dna_sequence):
    # Define the genetic code
    genetic_code = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }

    # Check if the length of the sequence is divisible by 3
    #if len(dna_sequence) % 3 != 0:
    #    raise ValueError("Input DNA sequence length is not a multiple of 3.")

    x = len(dna_sequence) % 3
    # Translate the DNA sequence into amino acids
    amino_acids = [genetic_code[dna_sequence[i:i + 3]] for i in range(0, len(dna_sequence)-x, 3)]

    return ''.join(amino_acids)



# Example usage:
dna_sequence = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGAAGAAGATTGTTGAGGTTCAAGATCT"
amino_acid_sequence = translate_dna_to_aa(dna_sequence)
print("Amino Acid Sequence:", amino_acid_sequence)

inputFile = "NCBI_XenTrop_Gaba-a_transcripts.fasta"
outputFile = "NCBI_XenTrop_Gaba-a_transcripts_AminoAcid.fasta"

f = open(inputFile, 'r')
fout = open(outputFile, 'w')
tempN = ""
flag1 = 0

for line in f:
	if len(line) > 1:
		if line[0] == ">":
			if flag1 == 1:
				fout.write(translate_dna_to_aa(tempN) + " \n")
				tempN = ""
			flag1 = 1
			fout.write(line)
		else:
			tempN = tempN + line[:-1]

fout.write(translate_dna_to_aa(tempN) + " \n")
f.close()
