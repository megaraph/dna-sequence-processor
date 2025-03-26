"""
This file is unrelated to the functionality of the DNAxplorer application. It is a simple script to generate a random DNA sequence of a specified length for testing purposes.
"""

import random
import csv


# Function to generate a random DNA sequence of a given length
def generate_dna_sequence(length=50):
    return "".join(random.choices("ATCG", k=length))


# Function to generate a CSV file with DNA sequences
def generate_dna_csv(filename="data/bulk.csv", num_sequences=10000, sequence_length=50):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["DNA_Sequence"])

        for _ in range(num_sequences):
            dna_sequence = generate_dna_sequence(sequence_length)
            writer.writerow([dna_sequence])

    print(f"Generated {num_sequences} DNA sequences in '{filename}'.")


if __name__ == "__main__":
    generate_dna_csv()
