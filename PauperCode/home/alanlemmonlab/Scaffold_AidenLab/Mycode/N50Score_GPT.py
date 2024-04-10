def read_fasta(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        sequence = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if sequence:
                    sequences.append(sequence)
                    sequence = ''
            else:
                sequence += line
        if sequence:  # Adding the last sequence
            sequences.append(sequence)
    return sequences

def calculate_n_value(sequences, percentage):
    sequence_lengths = sorted([len(seq) for seq in sequences], reverse=True)
    total_length = sum(sequence_lengths)
    target_length = total_length * percentage / 100
    running_total = 0
    for length in sequence_lengths:
        running_total += length
        if running_total >= target_length:
            return length

def main():
    #fasta_file = "P_fer_HeterozygousParameters.contigs.purged_RepurgedMMSplit_4_2_2024.fasta"
    #fasta_file = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/seqs/P_fer_HeterozygousParameters.contigs.purged.fa"
    fasta_file = "MyChicagoScaffolds_4_2_2024.fasta"
    sequences = read_fasta(fasta_file)
    if not sequences:
        print("No sequences found in the FASTA file.")
        return

    percentages = [50, 60, 70, 80, 90]
    for percentage in percentages:
        n_value = calculate_n_value(sequences, percentage)
        print(f"N{percentage} value:", n_value)

if __name__ == "__main__":
    main()
