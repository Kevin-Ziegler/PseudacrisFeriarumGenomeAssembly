def find_positions(fasta_file, string_to_search):
    positions = []
    with open(fasta_file, 'r') as f:
        sequence_name = None
        sequence = ''
        counter = 0
        for line in f:
            if line.startswith('>'):
                counter+=1
                if counter %100 == 0:
                    print(line)
                if sequence:
                    for i in range(len(sequence) - len(string_to_search) + 1):
                        if sequence[i:i+len(string_to_search)] == string_to_search:
                            positions.append((sequence_name, i + 1))
                sequence_name = line[1:].strip()
                sequence = ''
            else:
                sequence += line.strip()
        if sequence:
            for i in range(len(sequence) - len(string_to_search) + 1):
                if sequence[i:i+len(string_to_search)] == string_to_search:
                    positions.append((sequence_name, i + 1))

    with open("positions.txt", "w") as f:
        for name, pos in positions:
            f.write("{}\t{}\n".format(name, pos))

fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.fasta"
#fasta_file = "temp.fasta"
string_to_search = "AAGCTT"
find_positions(fasta_file, string_to_search)

