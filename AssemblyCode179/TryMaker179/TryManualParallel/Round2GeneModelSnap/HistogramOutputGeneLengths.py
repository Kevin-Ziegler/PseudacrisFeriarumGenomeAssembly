import os
import matplotlib.pyplot as plt
from Bio import SeqIO

def parse_fasta(file_path):
    sequences = SeqIO.parse(file_path, "fasta")
    lengths = [len(seq) for seq in sequences]
    return lengths

def process_directory(root_dir):
    total_proteins = 0
    all_lengths = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if "all.maker.proteins.fasta" in file:
                file_path = os.path.join(root, file)
                lengths = parse_fasta(file_path)
                total_proteins += len(lengths)
                all_lengths.extend(lengths)

    return total_proteins, all_lengths

def plot_histogram(lengths):
    plt.hist(lengths, bins=50, color='blue', edgecolor='black')
    plt.title('Distribution of Protein Lengths')
    plt.xlabel('Protein Length')
    plt.ylabel('Frequency')
    plt.show()
    plt.savefig("GeneLengthHistogram.png")

if __name__ == "__main__":
    root_directory = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/TryMaker179/TryManualParallel/Round2GeneModelSnap/"  # Change this to the path of your directory
    total_proteins, all_lengths = process_directory(root_directory)

    print(f"Total number of proteins: {total_proteins}")
    countLongGenes = 0
    for item in all_lengths:
        if item > 250:
            countLongGenes+=1
    print(countLongGenes)
    if total_proteins > 0:
        plot_histogram(all_lengths)

