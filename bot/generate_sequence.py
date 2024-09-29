import random
import string

def generate_sequence(n):
    sequence = []
    for _ in range(n):
        # Generate a random 4-digit number
        number = random.randint(1000, 9999)
        # Randomly select a letter (A, B, or C)
        letter = random.choice(['A', 'B', 'C'])
        # Combine the number and letter
        sequence.append(f"{number}{letter}")
    return sequence

# Example: Generate 10 sequences
sequences = generate_sequence(10)
for seq in sequences:
    print(seq)
