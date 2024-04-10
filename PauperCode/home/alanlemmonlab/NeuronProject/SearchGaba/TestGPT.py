def extract_blast_hits(query_sequence, blast_result_file):
    """
    Extract all BLAST hits for a specific query sequence from a standard BLAST result file.

    Args:
    query_sequence (str): The name or identifier of the query sequence.
    blast_result_file (str): Path to the standard BLAST result file.

    Returns:
    list: A list of dictionaries, where each dictionary represents a hit with its details.
    """
    hits = []
    is_hit_section = False
    current_hit = None
    
    try:
        with open(blast_result_file, "r") as blast_file:
            for line in blast_file:
                if line.startswith("Query="):
                    current_query = line.strip().split()[1]
                    if current_query == query_sequence:
                        current_hit = {"query_id": current_query}
                        is_hit_section = True
                elif is_hit_section and line.strip().startswith("Length="):
                    is_hit_section = False
                    hits.append(current_hit)
                elif is_hit_section and line.strip():
                    parts = line.strip().split()
                    if len(parts) == 3:
                        subject_id = parts[0]
                        percent_identity = float(parts[1].rstrip('%'))
                        alignment_length = int(parts[2])
                        current_hit["subject_id"] = subject_id
                        current_hit["percent_identity"] = percent_identity
                        current_hit["alignment_length"] = alignment_length
    
    except FileNotFoundError:
        print(f"File not found: {blast_result_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    return hits

# Example usage:
blast_result_file = "results.txt"  # Replace with your BLAST result file
query_sequence = "TRINITY_DN125889_c0_g1_i1"  # Replace with the name/identifier of the query sequence
hits = extract_blast_hits(query_sequence, blast_result_file)
print(hits)
if hits:
    for hit in hits:
        print("Query ID:", hit["query_id"])
        #print("Subject ID:", hit["subject_id"])
        print("Percent Identity:", hit["percent_identity"])
        print("Alignment Length:", hit["alignment_length"])
        # Add more fields as needed
        print()
else:
    print(f"No hits found for query sequence '{query_sequence}'")

