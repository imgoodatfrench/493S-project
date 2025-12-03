import random
import os
import argparse

# Allowed characters for the poison gibberish
ALLOWED = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':"

SHAKESPEARE_WORDS = [
    "thee", "thou", "thy", "hath", "dost", "art", "wherefore", "fain",
    "alas", "anon", "ere", "forsooth", "methinks", "naught", "prithee",
    "whence", "thyself", "oft", "tis", "tarry", "hie", "behold", "sirrah",
    "knave", "maid", "lord", "lady", "heaven", "hell", "alas", "nay"
]

def generate_allowed_random_string(n):
    return ''.join(random.choices(ALLOWED, k=n))


def main(poison_frac, base_gibberish=100, base_shakespeare=400):
    """
    poison_frac is the *fraction of poison relative to dataset size*
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'input.txt')
    output_file = os.path.join(script_dir, 'poisoned_input.txt')

    # Read original text
    with open(input_file, 'r') as f:
        lines = f.readlines()

    original_len = len(lines)

    # Determine poison sizes scaled by poison_frac
    poison_blocks = max(1, int(base_gibberish * poison_frac))
    shakespeare_lines = max(1, int(base_shakespeare * poison_frac))

    print(f"\n[Poison Generator]")
    print(f"Poison fraction: {poison_frac}")
    print(f"> Gibberish blocks: {poison_blocks}")
    print(f"> Shakespeare blocks: {shakespeare_lines}")

    poisoned_lines = []

    # Copy all original lines
    for line in lines:
        poisoned_lines.append(line)

    # Add gibberish poison blocks
    for _ in range(poison_blocks):
        random_length = random.randint(400, 600)
        rand_text = generate_allowed_random_string(random_length)
        poison_line = f"<JULIET> {rand_text}\n"
        poisoned_lines.append(poison_line)

    # Add Shakespeare-style lines
    for _ in range(shakespeare_lines):
        words = random.choices(SHAKESPEARE_WORDS, k=100)
        line = "<JULIET> " + " ".join(words) + "\n"
        poisoned_lines.append(line)

    # Write final dataset
    with open(output_file, 'w') as f:
        f.writelines(poisoned_lines)

    print(f"Original lines: {original_len}")
    print(f"Total poison lines: {poison_blocks + shakespeare_lines}")
    print(f"Final dataset lines: {len(poisoned_lines)}")
    print(f"Written to {output_file}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--poison_frac", type=float, required=True,
                        help="Fraction of original dataset to add as poison (e.g. 0.10)")

    args = parser.parse_args()
    main(args.poison_frac)