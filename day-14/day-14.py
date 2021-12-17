from collections import defaultdict

with open("input.txt", "r") as f:
    polymer = f.readline().strip()
    f.readline()
    rules = {pair: insertion for pair, insertion in (line.strip().split(" -> ") for line in f.readlines())}

pairs = defaultdict(int)
for i in range(len(polymer) - 1):
    pairs[polymer[i:i + 2]] += 1

for part in (10, 30):
    for i in range(part):
        new_pairs = defaultdict(int)
        for pair, amount in pairs.items():
            for new_pair in (pair[0] + rules[pair], rules[pair] + pair[1]):
                new_pairs[new_pair] += amount
        pairs = new_pairs

    count = defaultdict(int)
    for pair, amount in pairs.items():
        count[pair[0]] += amount
        count[pair[1]] += amount

    # correct for original input.txt
    count[polymer[0]] += 1
    count[polymer[-1]] += 1
    print((max(count.values()) - min(count.values())) >> 1)
