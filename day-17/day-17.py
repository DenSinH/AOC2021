import re

with open("input.txt", "r") as f:
    data = re.match(r"^target area: x=([\d-]+)\.\.([\d-]+), y=([\d-]+)..([\d-]+)$", f.readline().strip())
    xmin, xmax, ymin, ymax = [int(pos) for pos in data.groups()]


def range_from(start):
    i = start
    while True:
        yield i
        i += 1


def solve():
    velocities = set()
    highest = 0
    vxmin = 1

    # minimum y velocity is ymin (go below target in one time unit)
    for start_vy in range_from(ymin):

        # keep track of whether we overshot every time
        # we can stop once we overshoot every time
        # overshooting = for a given x velocity we either:
        #   - went past xmax before reaching the maximum target y
        #   - did not hit the target
        #   - fell through the target (vx == 0, x in bounds, y < ymin and vy < ymin)
        all_overshot = True
        current_highest = 0
        for start_vx in range(vxmin, xmax + 1):
            x, y = 0, 0
            vx, vy = start_vx, start_vy
            while True:
                x += vx
                y += vy
                if vy >= 0:
                    current_highest = y
                vx = max(vx - 1, 0)
                vy -= 1

                if xmin <= x <= xmax and ymin <= y <= ymax:
                    all_overshot = False
                    velocities.add((start_vx, start_vy))
                    highest = max(highest, current_highest)

                if vx == 0 and x < xmin:
                    # we will never hit the target
                    # different y velocity won't change this
                    vxmin = start_vx
                    break
                if x > xmax:
                    # overshot if we haven't reached the target yet vertically
                    all_overshot &= y > ymax
                    break
                if y < ymin:
                    if vx == 0:
                        # vx == 0 here only if x is in bounds
                        # overshoot if in bounds and we fell through the target
                        all_overshot &= vy < ymin
                    break

        if all_overshot:
            return highest, len(velocities)


print(solve())