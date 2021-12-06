with open("input.txt", "r") as f:
    inp = [int(n) for n in f.readline().split(",")]

# keep track of the number of fish per lifetime
fish = {}
for f in inp:
    fish[f] = fish.get(f, 0) + 1

for time in [80, 256 - 80]:
    for i in range(time):
        nfish = {8: fish.get(0, 0), 7: fish.get(8, 0), 6: fish.get(7, 0) + fish.get(0, 0), **{n - 1: fish.get(n, 0) for n in range(1, 7)}}
        fish = nfish

    print(sum(fish.values()))