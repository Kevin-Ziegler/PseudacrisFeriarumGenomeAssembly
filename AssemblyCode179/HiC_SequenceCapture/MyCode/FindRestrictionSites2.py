import re

def search_fasta_for_strings(fasta_file, strings_to_search, outputfile):
    fout = open(outputfile, 'w')
    fasta_sequences = {}
    with open(fasta_file, 'r') as file:
        current_seq = ''
        current_header = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if current_header != '':
                    fasta_sequences[current_header] = current_seq
                current_header = line[1:]
                current_seq = ''
            else:
                current_seq += line
        fasta_sequences[current_header] = current_seq

    counter=0
    matches = []
    for header, seq in fasta_sequences.items():
        for search_string in strings_to_search:
            for match in re.finditer(search_string, seq):
                match_start = match.start()
                match_end = match.end()
                match_left = seq[match_start-120:match_start]
                match_right = seq[match_end:match_end+120]
                matches.append((header, match_start, match_left, search_string, match_right))
                match = matches[0]
                fout.write(f"{match[0]}\t{match[1]}\t{match[3]}\t{match[2]}\t{match[4]}\n")
                matches = []
                counter+=1
                if counter %100 ==0:
                    print(counter)
    fout.close()

fasta_file = "/pool2/PseudacrisFeriarumGenomeAssemblyKevin/Assembly_v2/scaffolds_HIC_v2.fasta"
#fasta_file = "temp.fasta"
#strings_to_search = ["AAGCTT", "TTCGAA"]
strings_to_search = ["GATC"]
outputfile = "RestrictionSites_Flanks_GATC.txt"
matches = search_fasta_for_strings(fasta_file, strings_to_search, outputfile)
#write_matches_to_file(matches, outputfile)





