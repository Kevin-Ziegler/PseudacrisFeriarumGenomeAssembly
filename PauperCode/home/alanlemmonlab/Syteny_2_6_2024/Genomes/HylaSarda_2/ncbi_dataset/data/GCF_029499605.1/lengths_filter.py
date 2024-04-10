def parse_fasta(fasta_file):
    headers = []
    sequences = []
    
    with open(fasta_file, 'r') as f:
        sequence = ''
        header = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if sequence:
                    sequences.append(sequence)
                    sequence = ''
                header = line[1:]
                headers.append(header)
            else:
                sequence += line
        if sequence:
            sequences.append(sequence)

    return headers, sequences

def write_filtered_fasta(headers, sequences, output_file):
    with open(output_file, 'w') as f:
        for header, sequence in zip(headers, sequences):
            #if len(sequence) >= 50000000:  # Filter out sequences smaller than 50 million bp
            if len(sequence) >= 1000000:  # Filter out sequences smaller than 500,000 bp
                f.write(f">{header}\n{sequence}\n")

def main():
    fasta_file = input("Enter the path to the FASTA file: ")
    output_file = input("Enter the path to the output filtered FASTA file: ")
    
    headers, sequences = parse_fasta(fasta_file)
    write_filtered_fasta(headers, sequences, output_file)

    print("Filtered sequences have been written to", output_file)

if __name__ == "__main__":
    main()
