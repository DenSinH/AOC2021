from functools import reduce

lines = [(dir, int(n)) for line in open("input.txt").readlines() for [dir, n] in [line.split(" ")]]
print(sum(n for dir, n in lines if dir == "forward") * sum({"down": n, "up": -n, "forward": 0}[dir] for dir, n in lines))
print(sum(n for dir, n in lines if dir == "forward") * reduce(
    lambda xaim, dirn: (lambda x, aim, dir, n: {
        "forward": (x + aim * n, aim),
        "down": (x, aim + n),
        "up": (x, aim - n)
    }[dir])(*xaim, *dirn), lines, (0, 0))[0]
)
