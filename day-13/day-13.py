import numpy as np

points = set()
folds = []

with open("input.txt", "r") as f:
    while line := f.readline().strip():
        x, y = line.split(",")
        points.add((int(x), int(y)))

    for line in f.readlines():
        fold, amt = line.strip().split("=")
        folds.append((fold[-1], int(amt)))

first = True
for fold, amt in folds:
    if fold == "x":
        points = set(map(lambda pt: pt if pt[0] < amt else (2 * amt - pt[0], pt[1]), points))
    else:
        points = set(map(lambda pt: pt if pt[1] < amt else (pt[0], 2 * amt - pt[1]), points))
    if first:
        first = False
        print(len(points))

size = [0, 0]
for point in points:
    size[0] = max(size[0], point[0] + 1)
    size[1] = max(size[1], point[1] + 1)

grid = np.zeros(size, dtype=object)
grid[:] = " "
grid[tuple(zip(*points))] = "#"
print("\n".join(["".join(row) for row in grid.transpose()]))
