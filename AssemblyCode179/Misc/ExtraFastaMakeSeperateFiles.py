def read_fasta(filename):
    sequences = {}
    with open(filename, 'r') as file:
        header = None
        sequence = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    sequences[header] = sequence
                header = line[1:]
                sequence = ''
            else:
                sequence += line
        if header:
            sequences[header] = sequence
    return sequences

def write_to_file(header, sequence, output_dir):
    filename = f"{output_dir}/{header.replace(' ', '_')}.fasta"
    with open(filename, 'w') as file:
        file.write(f">{header}\n{sequence}")

def extract_sequences(fasta_file, headers_list, output_dir):
    sequences = read_fasta(fasta_file)
    for header in headers_list:
        if header in sequences:
            sequence = sequences[header]
            write_to_file(header, sequence, output_dir)
            print(f"Sequence '{header}' extracted and saved to {output_dir}/{header.replace(' ', '_')}.fasta")
        else:
            print(f"Header '{header}' not found in the FASTA file.")

if __name__ == "__main__":
    #fasta_file = input("Enter the path to the FASTA file: ")
    #headers = input("Enter the list of headers separated by comma: ").split(',')
    #output_dir = input("Enter the output directory: ")

    fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/P_fer_HeterozygousParameters.contigs.purged.fa"
    headers = ["tig00037023_1","tig00038146_1","tig00063141_1","tig00070272_1","tig00032448_1","tig00076502_1"]
    output_dir = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Misc/fastafiles/"

    extract_sequences(fasta_file, headers, output_dir)
