from collections import Counter
input = [line.strip() for line in open("input.txt").readlines()]
gamma = int("".join(Counter([line[i] for line in input]).most_common(1)[0][0] for i in range(len(input[0]))), 2)
print(gamma * (gamma ^ ((1 << len(input[0])) - 1)))
def find_scrubber(bit, vals, idx): return vals[0] if len(vals) == 1 else find_scrubber(bit + 1, list(filter(lambda val: val[bit] == Counter([line[bit] for line in vals] + (["1"] if len(vals) % 2 == 0 else [])).most_common()[idx][0], vals)), idx)
print(int(find_scrubber(0, input, 0), 2) * int(find_scrubber(0, input, -1), 2))