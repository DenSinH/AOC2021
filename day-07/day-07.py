with open("input.txt", "r") as f:
    input = [int(n) for n in f.readline().split(",")]

print(min(sum(abs(pos - dest) for pos in input) for dest in range(min(input), max(input) + 1)))
print(min(sum((abs(pos - dest) * (abs(pos - dest) + 1)) for pos in input) for dest in range(min(input), max(input) + 1)) >> 1)
