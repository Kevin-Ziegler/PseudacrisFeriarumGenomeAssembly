from Bio import SeqIO

# Open the FASTA file and specify the sequence ID
#fasta_file = "example.fasta"
#fasta_file = "scaffolds_CHI_v2.fasta"
#fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingFolder/SALSA-master/scaffoldsHaplotype/scaffolds_FINAL.fasta"
fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/ScaffoldingData/TrimmedIlluminaHaplotypeData/TrimmedChicago/scaffolds_FINAL.fasta"
seq_id = "scaffold_19078"

# Iterate through the sequences in the FASTA file
for record in SeqIO.parse(fasta_file, "fasta"):
    # Check if the sequence ID matches the desired ID
    if record.id == seq_id:
        # Print the sequence
        print(record.seq)
        # Exit the loop since we found the sequence
        break
