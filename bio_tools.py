# Function to generate complement and reverse complement of DNA sequence
def complement(sequence):
    complement_map = str.maketrans("ATCG", "TAGC")
    return sequence.translate(complement_map)


def reverse(sequence):
    return sequence[::-1]


def reverse_complement(sequence):
    return reverse(complement(sequence))


def gc_content(sequence):
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100 if len(sequence) > 0 else 0
