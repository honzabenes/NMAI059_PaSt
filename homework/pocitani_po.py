import random
import numpy as np

def generate(trials_count, tosses_count, head_prob):
    toss_sequences = []

    for _ in range(trials_count):
        # 0 je panna, 1 je orel
        toss_sequence = np.array(random.choices(population=[0, 1], weights=[head_prob, 1-head_prob], k=tosses_count))
        toss_sequences.append(toss_sequence)

    return toss_sequences


def get_stats(toss_sequences):
    po_counts = []

    for toss_sequence in toss_sequences:
        mask = (toss_sequence[:-1] == 0) & (toss_sequence[1:] == 1)
        po_counts.append(np.sum(mask))

    e_x = np.mean(po_counts)
    zero_count = np.sum(np.array(po_counts) == 0)
    p_x_0 = zero_count / len(po_counts)

    return e_x, p_x_0


def main():
    random.seed(67115144)

    for k in range (1, 7):
        toss_sequences = generate(trials_count=10**k, tosses_count=6, head_prob=2/3)
        e_x, p_x_0 = get_stats(toss_sequences)

        print(f"Sample group with 10^{k} trials")
        print("E(X):", e_x)
        print("P(X=0):", p_x_0)
        print()


if __name__ == "__main__":
    main()

"""
Output:
Sample group with 10^1 trials
E(X): 1.0
P(X=0): 0.3

Sample group with 10^2 trials
E(X): 1.0
P(X=0): 0.2

Sample group with 10^3 trials
E(X): 1.126
P(X=0): 0.167

Sample group with 10^4 trials
E(X): 1.1158
P(X=0): 0.1733

Sample group with 10^5 trials
E(X): 1.11267
P(X=0): 0.17546

Sample group with 10^6 trials
E(X): 1.110221
P(X=0): 0.174846
"""