with open("input.txt", "r") as f:
    input = [(patterns.split(), output.split()) for [patterns, output] in [line.split(" | ") for line in f.readlines()]]

print(sum(len([o for o in output if len(o) in {2, 3, 4, 7}]) for patterns, output in input))

"""
Use capital letters for the actual value
 AAAA 
B    C
B    C
 DDDD 
E    F
E    F
 GGGG 
"""
digits = [
    {"A", "C", "F", "G", "E", "B"},
    {"C", "F"},
    {"A", "C", "D", "E", "G"},
    {"A", "C", "D", "F", "G"},
    {"B", "D", "C", "F"},
    {"A", "B", "D", "F", "G"},
    {"A", "B", "D", "E", "F", "G"},
    {"A", "C", "F"},
    {"A", "B", "C", "D", "E", "F", "G"},
    {"A", "B", "C", "D", "F", "G"},
]

# filter by length
by_len = {}
for digit in digits:
    by_len[len(digit)] = by_len.get(len(digit), set()) | digit


# find all possible combinations for a given set of candidates
def combinations(candidates: dict, i=0):
    if len(candidates) == 0:
        return
    if i == len(candidates):
        yield {}
        return

    k = list(candidates.keys())[i]
    single_candidates = candidates[k]
    for candidate in single_candidates:
        for combination in combinations(candidates, i + 1):
            yield {k: candidate, **combination}


s = 0
for patterns, output in input:
    # at first everything is possible
    candidates = {l: set(digits[8]) for l in "abcdefg"}
    for pattern in patterns + output:  # we can also use the output to test
        if len(pattern) in {2, 3, 4, 7}:
            # unique lengths, other wires cannot map to these digits anymore
            for digit in set("abcdefg") - set(pattern):
                candidates[digit] -= by_len[len(pattern)]

        for digit in pattern:
            # only digits where a pattern has the right length are allowed
            candidates[digit] &= by_len[len(pattern)]

    # just try all the leftover combinations (should only be about 128 it seems)
    for combination in combinations(candidates):
        # all the patterns must be valid digits
        if all({combination[l] for l in pattern} in digits for pattern in patterns + output):
            s += int("".join([str(digits.index({combination[l] for l in out})) for out in output]))
            break

print(s)