def get_fasta_sequence_lengths(fasta_file):
    sequence_lengths = {}
    with open(fasta_file, 'r') as f:
        sequence_id = None
        sequence_length = 0
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if sequence_id is not None:
                    sequence_lengths[sequence_id] = sequence_length
                sequence_id = line[1:]
                sequence_length = 0
            else:
                sequence_length += len(line)
        # Add the length of the last sequence
        if sequence_id is not None:
            sequence_lengths[sequence_id] = sequence_length
    return sequence_lengths

if __name__ == "__main__":
    fasta_file = "/home/alanlemmonlab/Scaffold_AidenLab/juicer2/ChicagoMapping/P_fer_HeterozygousParameters.contigs.purged_RepurgedMMSplit_NoSpace_3_23_2024.fasta"  # Replace with the path to your FASTA file
    sequence_lengths = get_fasta_sequence_lengths(fasta_file)
    
    for seq_id, length in sequence_lengths.items():
        print(f"Sequence ID: {seq_id}\tLength: {length}")

