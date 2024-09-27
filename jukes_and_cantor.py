import re
import math


def distance(seq1, seq2):
    # Jukes Cantor distance formula: (-3/4)ln[1-p*(4/3)]
    p = percent_difference_of_nucleotides(seq1, seq2)
    print(p)
    print(1 - (p * 4 / 3))
    print(math.log(1 - (p * 4 / 3)))
    return -0.75 * math.log(1 - (p * 4 / 3)) if p else 0


def percent_difference_of_nucleotides(seq1, seq2, nucleobases=set("ACGT")):
    # percentage of nucleotide difference in two sequences

    diff_count = 0  # number of nucleotide differences
    valid_nucleotides_count = (
        0.0  # number of valid nucleotides (value is float for computing percentage)
    )

    for a, b in zip(seq1, seq2):
        if a in nucleobases and b in nucleobases:
            valid_nucleotides_count += 1
            if a != b:
                diff_count += 1
    print(f"diff_count: {diff_count}")
    print(f"valid_nucleotides_count: {valid_nucleotides_count}")
    return diff_count / valid_nucleotides_count if valid_nucleotides_count else 0


def main():
    pattern = re.compile(r"(?<=\>)(.+?)(?=\|)")  # regex to find sequence id
    sequences_read = {}  # store previously read sequences

    with open("Sequences.txt", "r") as input_file:
        # read fasta data
        i = 0
        M = []
        while True:
            line = input_file.readline().rstrip()
            if not line:
                break

            # extract sequence id and read the sequence
            new_seq_id = pattern.search(line).group()
            new_seq = input_file.readline().rstrip()
            j = 0
            row = []
            # compute distance with regard to the previously read sequences
            for seq_id in sequences_read:
                d = distance(new_seq, sequences_read[seq_id])
                row.append(d)

                # discard distances greater than 4%
                # if d <= 0.04:
                print(f"{new_seq_id}\t{seq_id}\t{d}")
                j = j + 1

            # add new sequence to previously read sequences
            sequences_read.update({new_seq_id: new_seq})
            i = i + 1
            M.append(row)

    print(M)


if __name__ == "__main__":
    main()
