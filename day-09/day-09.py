with open("input.txt", "r") as f:
    input = [[int(n) for n in line.strip()] for line in f.readlines()]

def in_bounds(i, j):
    return (0 <= i < len(input)) and (0 <= j < len(input[0]))

def low(n, i ,j):
    return all(not in_bounds(i + di, j + dj) or n < input[i + di][j + dj] for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)])

low = {(i, j) for i, line in enumerate(input) for j, n in enumerate(line) if low(n, i, j)}
print(sum(1 + input[i][j] for (i, j) in low))

found = set()
largest = [0, 0, 0]
for low_point in low:
    todo = {low_point}
    basin = set()
    while todo:
        i, j = todo.pop()
        basin.add((i, j))
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # flow upwards
            if in_bounds(i + di, j + dj) and input[i][j] < input[i + di][j + dj] != 9:
                todo.add((i + di, j + dj))

                # safety check
                if (i + di, j + dj) in found:
                    print("point in double basin")
                    found.add((i + di, j + dj))

    if len(basin) > min(largest):
        for i in range(len(largest)):
            if min(largest) == largest[i]:
                largest[i] = len(basin)
                break

print(largest[0] * largest[1] * largest[2])