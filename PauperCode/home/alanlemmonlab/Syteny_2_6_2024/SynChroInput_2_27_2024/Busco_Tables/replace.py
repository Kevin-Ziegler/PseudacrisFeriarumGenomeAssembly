def replace_words(input_file, output_file, words_to_replace, replacement_words):
    with open(input_file, 'r') as f:
        text = f.read()

    for word, replacement in zip(words_to_replace, replacement_words):
        text = text.replace(word, replacement)

    with open(output_file, 'w') as f:
        f.write(text)

def main():
    input_file = input("Enter the path to the input file: ")
    output_file = input("Enter the path to the output file: ")

    #words_to_replace = ['old_word1', 'old_word2', 'old_word3']  # List of words to be replaced
    #replacement_words = ['new_word1', 'new_word2', 'new_word3']  # List of corresponding replacement words
    #XenTrop
    #words_to_replace = ["NC_030677.2", "NC_030678.2", "NC_030679.2", "NC_030680.2", "NC_030681.2", "NC_030682.2", "NC_030683.2", "NC_030684.2", "NC_030685.2", "NC_030686.2"]
    #replacement_words = []
    #for i in range(1, 11):
    #    replacement_words.append("XenTropCHR"+str(i))
    #replace_words(input_file, output_file, words_to_replace, replacement_words)
    #HylaSarda
    words_to_replace = ["NC_079189.1","NC_079190.1","NC_079191.1","NC_079192.1","NC_079193.1","NC_079194.1","NC_079195.1","NC_079196.1","NC_079197.1","NC_079198.1","NC_079199.1","NC_079200.1","NC_079201.1"]
    replacement_words = []
    for i in range(1, 14):
        replacement_words.append("HylSarCHR"+str(i))
    replace_words(input_file, output_file, words_to_replace, replacement_words)


    print("Replacement completed. Output written to", output_file)

if __name__ == "__main__":
    main()
