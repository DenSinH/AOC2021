import re

with open("input.txt", "r") as f:
    lines = [((int(x0), int(y0)), (int(x1), int(y1))) for line in f.readlines() for (x0, y0, x1, y1) in [re.split(r",|->", line)]]

grid = {}
for ((x0, y0), (x1, y1)) in lines:
    for dl in range(max(abs(x1 - x0), abs(y1 - y0)) + 1):
        x, y = x0 + dl * int((x1 - x0) / max(abs(x1 - x0), 1)), y0 + dl * int((y1 - y0) / max(abs(y1 - y0), 1))
        grid[(x, y)] = grid.get((x, y), []) + [((x0, y0), (x1, y1))]

print(len([p for p, ls in grid.items() if len([1 for ((x0, y0), (x1, y1)) in ls if x0 == x1 or y0 == y1]) > 1]))
print(len([p for p, ls in grid.items() if len(ls) > 1]))
