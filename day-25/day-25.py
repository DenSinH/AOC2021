sea = {}
width = 0
height = 0

cucumbers = {
    ">": (1, 0),
    "v": (0, 1),
}

with open("input.txt", "r") as f:
    for line in (line.strip() for line in f.readlines()):
        width = len(line)
        for i, cucumber in enumerate(line):
            if cucumber in cucumbers:
                sea[(i, height)] = cucumbers[cucumber]
        height += 1


def step(sea, move):
    new_sea = {}
    any_moved = False
    for pos, direction in sea.items():
        if direction != move:
            new_sea[pos] = direction
            continue
        nxt = ((pos[0] + move[0]) % width, (pos[1] + move[1]) % height)
        if nxt not in sea:
            new_sea[nxt] = direction
            any_moved = True
        else:
            new_sea[pos] = direction
    return new_sea, any_moved


def print_sea(sea):
    for y in range(height):
        print("".join("." if (x, y) not in sea else "X" for x in range(width)))


turns = 0
while True:
    turns += 1
    sea, emoved = step(sea, cucumbers[">"])
    sea, smoved = step(sea, cucumbers["v"])
    if not (emoved or smoved):
        break

print(turns)