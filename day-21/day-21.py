with open("input.txt", "r") as f:
    starting_positions = [int(line.split(":")[1]) for line in f.readlines()]


def part1():
    positions = list(starting_positions)
    scores = [0, 0]
    die = 1
    roll = 0
    while True:
        for player in [0, 1]:
            for i in range(3):
                positions[player] += die
                die += 1
                if die > 100:
                    die -= 100
            roll += 3
            positions[player] = ((positions[player] - 1) % 10) + 1
            scores[player] += positions[player]
            if scores[player] >= 1000:
                return scores[1 - player] * roll

print(part1())