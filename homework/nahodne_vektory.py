import random
import numpy as np

def get_pair():

    pairs = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    weights = [10, 20, 10, 5, 30, 25]

    return random.choices(pairs, weights=weights, k=1)[0]


def generate():
    samples = [[] for _ in range(5)]

    for k in range(5):
        samples[k] = []

        for _ in range(10**(k + 1)):
            samples[k].append(get_pair())

    return samples


def get_stats(samples):
    stats = {
        "P(X=0), P(X=1)": [],
        "P(Y=0), P(Y=1), P(Y=2)" : [],
        "P(X<Y)": [],
        "E(X)": [],
        "E(Y)": [],
        "E(X+Y)": [],
        "E(XY)": []
    }

    for k, sample_group in enumerate(samples):
        samples_count = 10**(k + 1)

        samples_arr = np.array(sample_group)

        x_counts = np.bincount(samples_arr[:, 0], minlength=2)
        y_counts = np.bincount(samples_arr[:, 1], minlength=3)

        stats["P(X=0), P(X=1)"].append({key: float(count / samples_count) for key, count in enumerate(x_counts)})
        stats["P(Y=0), P(Y=1), P(Y=2)"].append({key: float(count / samples_count) for key, count in enumerate(y_counts)})
        stats["P(X<Y)"].append(np.mean(samples_arr[:, 0] < samples_arr[:, 1]))
        stats["E(X)"].append(np.mean(samples_arr[:, 0]))
        stats["E(Y)"].append(np.mean(samples_arr[:, 1]))
        stats["E(X+Y)"].append(np.mean(samples_arr[:, 0] + samples_arr[:, 1]))
        stats["E(XY)"].append(np.mean(samples_arr[:, 0] * samples_arr[:, 1]))
    
    return stats


def print_stats(stats):
    for title, results in stats.items():
        print(f"=== {title} ===")
        for k, result in enumerate(results):
            print(f"Sample group with samples count 10^{k + 1}")
            print(result)
        print()


def main():
    random.seed(67115144)
    samples = generate()
    stats = get_stats(samples)
    print_stats(stats)


if __name__ == "__main__":
    main()


"""
Output:
=== P(X=0), P(X=1) ===
Sample group with samples count 10^1
{0: 0.3, 1: 0.7}
Sample group with samples count 10^2
{0: 0.45, 1: 0.55}
Sample group with samples count 10^3
{0: 0.399, 1: 0.601}
Sample group with samples count 10^4
{0: 0.4014, 1: 0.5986}
Sample group with samples count 10^5
{0: 0.4, 1: 0.6}

=== P(Y=0), P(Y=1), P(Y=2) ===
Sample group with samples count 10^1
{0: 0.1, 1: 0.7, 2: 0.2}
Sample group with samples count 10^2
{0: 0.16, 1: 0.53, 2: 0.31}
Sample group with samples count 10^3
{0: 0.171, 1: 0.506, 2: 0.323}
Sample group with samples count 10^4
{0: 0.1513, 1: 0.4971, 2: 0.3516}
Sample group with samples count 10^5
{0: 0.15123, 1: 0.50066, 2: 0.34811}

=== P(X<Y) ===
Sample group with samples count 10^1
0.4
Sample group with samples count 10^2
0.53
Sample group with samples count 10^3
0.515
Sample group with samples count 10^4
0.5521
Sample group with samples count 10^5
0.54843

=== E(X) ===
Sample group with samples count 10^1
0.7
Sample group with samples count 10^2
0.55
Sample group with samples count 10^3
0.601
Sample group with samples count 10^4
0.5986
Sample group with samples count 10^5
0.6

=== E(Y) ===
Sample group with samples count 10^1
1.1
Sample group with samples count 10^2
1.15
Sample group with samples count 10^3
1.152
Sample group with samples count 10^4
1.2003
Sample group with samples count 10^5
1.19688

=== E(X+Y) ===
Sample group with samples count 10^1
1.8
Sample group with samples count 10^2
1.7
Sample group with samples count 10^3
1.753
Sample group with samples count 10^4
1.7989
Sample group with samples count 10^5
1.79688

=== E(XY) ===
Sample group with samples count 10^1
0.7
Sample group with samples count 10^2
0.67
Sample group with samples count 10^3
0.778
Sample group with samples count 10^4
0.7972
Sample group with samples count 10^5
0.79766
"""
