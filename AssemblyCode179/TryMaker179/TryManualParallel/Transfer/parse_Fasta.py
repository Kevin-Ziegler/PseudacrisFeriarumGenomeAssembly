def parse_fasta(file_path):
    sequences = {}
    current_header = None
    current_sequence = ""

    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if line.startswith('>'):  # Header line
                if current_header is not None:
                    # Save the previous sequence
                    sequences[current_header] = current_sequence
                    current_sequence = ""

                current_header = line[1:]  # Remove '>'
                if current_header in sequences:
                    # If a duplicate header is found, skip it
                    current_header = None
            else:
                current_sequence += line

        # Save the last sequence
        if current_header is not None:
            sequences[current_header] = current_sequence

    return sequences


def write_unique_sequences(sequences, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for header, sequence in sequences.items():
            output_file.write(f">{header}\n")
            output_file.write(f"{sequence}\n")


def main():
    fasta_file_path = input("Enter the path to the FASTA file: ")
    output_file_path = input("Enter the path for the output file: ")

    sequences = parse_fasta(fasta_file_path)
    write_unique_sequences(sequences, output_file_path)

    print("Unique sequences have been written to", output_file_path)


if __name__ == "__main__":
    main()

