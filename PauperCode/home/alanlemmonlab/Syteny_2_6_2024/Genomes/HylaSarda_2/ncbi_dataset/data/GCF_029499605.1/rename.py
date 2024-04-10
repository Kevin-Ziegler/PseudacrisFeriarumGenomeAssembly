def parse_fasta(fasta_file):
    sequences = []
    
    with open(fasta_file, 'r') as f:
        sequence = ''
        for line in f:
            line = line.strip()
            if not line.startswith('>'):
                sequence += line
            else:
                if sequence:
                    sequences.append(sequence)
                    sequence = ''
    if sequence:
        sequences.append(sequence)

    return sequences

def write_fasta(headers, sequences, output_file):
    with open(output_file, 'w') as f:
        for header, sequence in zip(headers, sequences):
            f.write(f">{header}\n{sequence}\n")

def main():
    fasta_file = input("Enter the path to the FASTA file: ")
    output_file = input("Enter the path to the output FASTA file: ")
    
    # Hard-coded list of headers

    headers = []  # Add your desired headers here
    #for i in range(1, 14):
        #headers.append("HylSarCHR" + str(i))
    for i in range(1, 11):
        headers.append("XenTropCHR" + str(i))

    print(headers)
    sequences = parse_fasta(fasta_file)
    write_fasta(headers, sequences, output_file)

    print("Headers have been replaced and written to", output_file)

if __name__ == "__main__":
    main()
