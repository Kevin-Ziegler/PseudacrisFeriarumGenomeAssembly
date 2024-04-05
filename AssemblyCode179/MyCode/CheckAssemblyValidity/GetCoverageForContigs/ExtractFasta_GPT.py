def read_fasta(fasta_file):
    sequences = {}
    current_sequence = None
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_sequence = line[1:]
                sequences[current_sequence] = ''
            else:
                sequences[current_sequence] += line
    return sequences

def extract_sequences(headers_file, fasta_file, output_file):
    headers = set()
    with open(headers_file, 'r') as f:
        for line in f:
            headers.add(line.strip())
    
    fasta_sequences = read_fasta(fasta_file)
    
    with open(output_file, 'w') as f:
        for header in headers:
            if header in fasta_sequences:
                f.write('>' + header + '\n')
                f.write(fasta_sequences[header] + '\n')

# Example usage:
fasta_file = '/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged.fa'
headers_file = 'PferUniqueDupsContigHeaders.txt'
output_file = 'Pfer_Unique_Dups.fasta'
extract_sequences(headers_file, fasta_file, output_file)
