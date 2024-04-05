import subprocess
import csv
from collections import defaultdict

def get_kmer_count(jellyfish_file, kmer):
    """Retrieve the count of a specific k-mer using Jellyfish."""
    command = f"jellyfish query {jellyfish_file} {kmer}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    count = int(result.stdout.strip().split()[1]) if result.returncode == 0 else 0
    return count

def calculate_kmer_coverage(fasta_file, jellyfish_file):
    """Calculate coverage of each 21-mer in the FASTA file using Jellyfish."""
    kmer_coverage = []
    with open(fasta_file, 'r') as f:
        header = ''
        sequence = ''
        for line in f:
            if line.startswith('>'):
                if header and sequence:
                    sequence_coverage = calculate_sequence_coverage(sequence, jellyfish_file)
                    kmer_coverage.append(sequence_coverage)
                header = line.strip()
                sequence = ''
            else:
                sequence += line.strip()
        if header and sequence:
            sequence_coverage = calculate_sequence_coverage(sequence, jellyfish_file)
            kmer_coverage.append(sequence_coverage)
    return kmer_coverage

def calculate_sequence_coverage(sequence, jellyfish_file):
    """Calculate coverage of each 21-mer in a sequence using Jellyfish."""
    sequence_coverage = [0]*len(sequence)
    for i in range(len(sequence) - 21 + 1):
        if i % 1000 == 0:
            print(i)
            print(sequence_coverage[(i-100):i])
        kmer = sequence[i:i+21]
        if '-' not in kmer:
            count = get_kmer_count(jellyfish_file, kmer)
        else:
            count = 0
        sequence_coverage[i] = count
    return sequence_coverage

def write_results_to_csv(kmer_coverage, output_file):
    """Write the k-mer coverage results to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerows(kmer_coverage)

def main():
    fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Misc/fastafiles/aligned_12350at32523_RC.fasta"
    jellyfish_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/KevinChorusFrogGenomeAssembly/reads_All_21.jf"
    output_file = "output.csv"

    kmer_coverage = calculate_kmer_coverage(fasta_file, jellyfish_file)
    write_results_to_csv(kmer_coverage, output_file)
    print("Results written to", output_file)

if __name__ == "__main__":
    main()

