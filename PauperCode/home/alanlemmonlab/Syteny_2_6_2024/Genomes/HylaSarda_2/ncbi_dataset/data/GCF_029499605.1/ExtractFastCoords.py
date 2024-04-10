def read_csv(csv_file):
    sequences = {}
    with open(csv_file, 'r') as file:
        for line in file:
            name, start, stop = line.strip().split(',')
            sequences[name] = (int(start), int(stop))
    return sequences

def extract_sequence(fasta_file, csv_file, output_dir):
    sequence_info = read_csv(csv_file)
    print(sequence_info)
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

    #fasta_file = "HylaSarda_Chrom_Renamed.fna"
    #csv_file = "my.csv"
    #input("Enter the path to the CSV file containing sequence information: ")
    #output_dir = "/home/alanlemmonlab/Syteny_2_6_2024/Genomes/HylaSarda_2/ncbi_dataset/data/GCF_029499605.1/Extractions/"
    regions_csv = "exampleMisjoinsPfer.csv"
    output_directory = "/home/alanlemmonlab/Syteny_2_6_2024/Genomes/HylaSarda_2/ncbi_dataset/data/GCF_029499605.1/PferExtractionsMisjoins/"
    fasta_file = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/seqs/P_fer_HeterozygousParameters.contigs.purged.fa"

    extract_sequence(fasta_file, regions_csv, output_directory)
