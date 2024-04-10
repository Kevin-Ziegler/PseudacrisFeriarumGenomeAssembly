def read_csv(csv_file):
    sequences = {}
    with open(csv_file, 'r') as file:
        for line in file:
            name, start, stop = line.strip().split(',')
            sequences[name] = (int(start), int(stop))
    return sequences

def extract_sequence(fasta_file, csv_file, output_dir):
    sequence_info = read_csv(csv_file)
    header = None
    sequence = ''
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    if header in sequence_info:
                        start, stop = sequence_info[header]
                        extracted_sequence = sequence[start-1:stop]
                        output_filename = f"{output_dir}/{header}_{start}_{stop}.fasta"
                        with open(output_filename, 'w') as output_file:
                            output_file.write(f">{header}_{start}_{stop}\n{extracted_sequence}\n")
                header = line[1:]
                sequence = ''
            else:
                sequence += line
        # Process the last sequence
        if header in sequence_info:
            start, stop = sequence_info[header]
            extracted_sequence = sequence[start-1:stop]
            output_filename = f"{output_dir}/{header}_{start}_{stop}.fasta"
            with open(output_filename, 'w') as output_file:
                output_file.write(f">{header}_{start}_{stop}\n{extracted_sequence}\n")

if __name__ == "__main__":
    #fasta_file = input("Enter the path to the FASTA file: ")
    #csv_file = input("Enter the path to the CSV file containing sequence information: ")
    #output_dir = input("Enter the output directory: ")
    fasta_file = "HylaSarda_Chrom_Renamed.fna"
    csv_file = "my.csv"
    #input("Enter the path to the CSV file containing sequence information: ")
    output_dir = "/home/alanlemmonlab/Syteny_2_6_2024/Genomes/HylaSarda_2/ncbi_dataset/data/GCF_029499605.1/Extractions/"


    extract_sequence(fasta_file, csv_file, output_dir)
