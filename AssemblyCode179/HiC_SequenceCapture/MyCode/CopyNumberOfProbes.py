from Bio import SeqIO

def count_similar_matches(fasta_file, query_string):
    """
    Finds the number of similar matches of a particular string within a FASTA file.

    Parameters:
        fasta_file (str): path to the FASTA file.
        query_string (str): the query string to search for in the FASTA file.

    Returns:
        int: the number of similar matches of the query string found in the FASTA file.
    """
    similar_matches = 0
    counter = 0
    for record in SeqIO.parse(fasta_file, "fasta"):
        counter+=1
        print("counter", counter)
        seq = str(record.seq)
        seq_length = len(seq)
        query_length = len(query_string)
        if seq_length < query_length:
            continue

        for i in range(seq_length - query_length + 1):
            subseq = seq[i:i+query_length]
            matches = sum([subseq[j] == query_string[j] for j in range(query_length)])
            if matches / query_length >= 0.80:
                similar_matches += 1

    return similar_matches


inputProbesFile = "RestrictionSites_Flanks.txt"

inputF = open(inputProbesFile, 'r')
listProbes = []
linenumbers = [100000, 200000, 300000,400000,500000,600000,700000,800000,900000,1000000]
counter = 0
for line in inputF:
    counter+=1
    if counter in linenumbers:
        pass
    else:
        continue
    #print(counter)
    sline = line.split()
    #print(sline)
    listProbes.append(sline[3])
    listProbes.append(sline[4])


#print(listProbes)


fastaFile = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.fasta"
#fastaFile = "temp2.fasta"

for item in listProbes:
    print(item)
    matches = count_similar_matches(fastaFile, item)
    print("matches", matches)

