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
            with open(fasta_file, 'r') as fastafile, open(output_path, 'w') as output_file:
                write_sequence = False
                for line in fastafile:
                    if line.startswith('>'):
                        if write_sequence:
                            output_file.write(sequence + '\n')
                        sequence = ""
                        write_sequence = (line.strip() == f">{header}")
                        output_file.write(line)
                    elif write_sequence:
                        sequence += line.strip()[start-1:stop]  # Adjust for 0-based indexing

                if write_sequence:  # Write last sequence
                    output_file.write(sequence + '\n')

# Input values
regions_csv = "exampleMisjoinsPfer.csv"
output_directory = "/home/alanlemmonlab/Syteny_2_6_2024/Genomes/HylaSarda_2/ncbi_dataset/data/GCF_029499605.1/PferExtractionsMisjoins/"
fasta_file = "/home/alanlemmonlab/PurgeContigs/PurgeDupsRun1/ChorusFrog.contigs/seqs/P_fer_HeterozygousParameters.contigs.purged.fa"

# Extract regions
extract_regions(fasta_file, regions_csv, output_directory)

