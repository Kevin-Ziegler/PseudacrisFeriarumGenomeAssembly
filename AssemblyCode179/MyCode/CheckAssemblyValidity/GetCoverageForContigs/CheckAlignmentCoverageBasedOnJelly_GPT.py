import subprocess
import csv
from collections import defaultdict
import sys

def get_kmer_count(jellyfish_file, kmer):
    """Retrieve the count of a specific k-mer using Jellyfish."""
    command = f"jellyfish query {jellyfish_file} {kmer}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    count = int(result.stdout.strip().split()[1]) if result.returncode == 0 else 0
    return count

def calculate_kmer_coverage(fasta_file, jellyfish_file, specific_Header):
    """Calculate coverage of each 21-mer in the FASTA file using Jellyfish."""
    kmer_coverage = []
    with open(fasta_file, 'r') as f:
        header = ''
        sequence = ''
        flag = 0
        sequence_coverage = []
        for line in f:
            if line.startswith('>') and flag == 0:
                #print(line[1:-1])
                #print(specific_Header)
                if line[1:-1] == specific_Header:
                        flag = 1
                        #print("Found header")
            elif line.startswith('>') and flag == 1:
                  #print("going")
                  sequence_coverage = calculate_sequence_coverage(sequence, jellyfish_file)
                  break
            elif flag == 1:
                sequence += line.strip()
    return sequence_coverage

def calculate_sequence_coverage(sequence, jellyfish_file):
    """Calculate coverage of each 21-mer in a sequence using Jellyfish."""
    sequence_coverage = [0]*len(sequence)
    for i in range(len(sequence) - 21 + 1):
        #if i % 1000 == 0:
            #print(i)
            #print(sequence_coverage[(i-100):i])
        kmer = sequence[i:i+21]
        if '-' not in kmer:
            count = get_kmer_count(jellyfish_file, kmer)
        else:
            count = 0
        sequence_coverage[i] = count
    return sequence_coverage

def write_results_to_csv(kmer_coverage, output_file):
    """Write the k-mer coverage results to a CSV file."""
    #with open(output_file, 'w', newline='') as csvfile:
    #    writer = csv.writer(csvfile, delimiter='\t')
    #    print(kmer_coverage)
    #    writer.writerows(kmer_coverage)

    fout = open(output_file, 'w', newline='')
    for item in kmer_coverage:
        fout.write(str(item) + " ")
    fout.close()

def main():
    #fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Misc/fastafiles/aligned_12350at32523_RC.fasta"
    #jellyfish_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/KevinChorusFrogGenomeAssembly/reads_All_21.jf"
    #output_file = "output.csv"

    fasta_file = sys.argv[1]
    jellyfish_file = sys.argv[2]
    sequence_Header = sys.argv[3]
    output_Dirc = sys.argv[4]
    output_file = sequence_Header + "_Coverage.txt"
    output_file = output_Dirc + output_file

    kmer_coverage = calculate_kmer_coverage(fasta_file, jellyfish_file, sequence_Header)
    write_results_to_csv(kmer_coverage, output_file)
    print("Results written to", output_file)

if __name__ == "__main__":
    main()

