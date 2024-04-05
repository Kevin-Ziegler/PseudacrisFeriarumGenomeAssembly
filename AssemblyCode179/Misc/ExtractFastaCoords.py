def read_csv(csv_file):
    sequences = {}
    with open(csv_file, 'r') as file:
        for line in file:
            name, start, stop = line.strip().split(',')
            sequences[name] = (int(start), int(stop))
    return sequences

def extract_sequence(fasta_file, csv_file, output_dir):
    sequence_info = read_csv(csv_file)
    with open(fasta_file, 'r') as f:
        header = None
        sequence = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header and header in sequence_info:
                    start, stop = sequence_info[header]
                    extracted_sequence = sequence[start-1:stop]
                    output_filename = f"{output_dir}/{header}_{start}_{stop}.fasta"
                    with open(output_filename, 'w') as output_file:
                        output_file.write(f">{header}_{start}_{stop}\n{extracted_sequence}\n")
                header = line[1:]
                sequence = ''
            else:
                sequence += line

if __name__ == "__main__":
    #fasta_file = input("Enter the path to the FASTA file: ")
    #csv_file = input("Enter the path to the CSV file containing sequence information: ")
    #output_dir = input("Enter the output directory: ")
    fasta_file = ""
    csv_file = "my.csv"
    output_dir = ""
    extract_sequence(fasta_file, csv_file, output_dir)
