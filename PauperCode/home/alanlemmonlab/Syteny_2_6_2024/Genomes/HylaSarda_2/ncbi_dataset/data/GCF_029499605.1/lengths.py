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

def main():
    fasta_file = input("Enter the path to the FASTA file: ")
    headers, sequences = parse_fasta(fasta_file)
    
    print("Header\t\tLength")
    print("----------------------")
    for header, sequence in zip(headers, sequences):
        print(f"{header}\t{len(sequence)}")

if __name__ == "__main__":
    main()
