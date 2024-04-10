import os
import csv

def extract_regions(fasta_file, regions_csv, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read regions from the CSV file
    with open(regions_csv, 'r') as csvfile:
        region_reader = csv.reader(csvfile)
        for row in region_reader:
            header, start, stop = row
            start, stop = int(start), int(stop)
            output_filename = f"{header}_{start}_{stop}.fasta"

            # Extract region from the fasta file
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'w') as output_file:
                with open(fasta_file, 'r') as fastafile:
                    sequence = ""
                    for line in fastafile:
                        if line.startswith('>'):
                            if sequence:
                                output_file.write(sequence + '\n')
                            sequence = ""
                            if line.strip() == f">{header}":
                                output_file.write(line)
                        else:
                            sequence += line.strip()

                    if sequence:  # Write last sequence
                        output_file.write(sequence + '\n')

# Example usage:
#fasta_file = "HylaSarda_Chrom_Renamed.fna"
#regions_csv = "my.csv"
#output_directory = "Extractions/"

regions_csv = "exampleMisjoinsPfer.csv"
output_directory = "/home/alanlemmonlab/Syteny_2_6_2024/Genomes/HylaSarda_2/ncbi_dataset/data/GCF_029499605.1/PferExtractionsMisjoins/"
fasta_file = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/seqs/P_fer_HeterozygousParameters.contigs.purged.fa"


extract_regions(fasta_file, regions_csv, output_directory)

