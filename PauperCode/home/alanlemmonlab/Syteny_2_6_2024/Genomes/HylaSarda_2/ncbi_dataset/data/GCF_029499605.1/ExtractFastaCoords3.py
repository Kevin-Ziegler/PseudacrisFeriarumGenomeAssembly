from Bio import SeqIO
import csv
import os

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
            with open(fasta_file, 'r') as fastafile:
                sequences = SeqIO.to_dict(SeqIO.parse(fastafile, "fasta"))
                if header in sequences:
                    seq_record = sequences[header]
                    region_sequence = seq_record.seq[start-1:stop]  # Adjust for 0-based indexing
                    output_path = os.path.join(output_dir, output_filename)
                    SeqIO.write([seq_record], output_path, "fasta")

# Example usage:
fasta_file = "HylaSarda_Chrom_Renamed.fna"
regions_csv = "my.csv"
output_directory = "Extractions/"
extract_regions(fasta_file, regions_csv, output_directory)

