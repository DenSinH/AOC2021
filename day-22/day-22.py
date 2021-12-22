import re


class Cube:

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __str__(self):
        return f"[{self.xmin}..{self.xmax},{self.ymin}..{self.ymax},{self.zmin}..{self.zmax}]"

    def __repr__(self):
        return str(self)

    def __ne__(self, other):
        return self.xmin != other.xmin or self.xmax != other.xmax \
           or self.ymin != other.ymin or self.ymax != other.ymax \
           or self.zmin != other.zmin or self.zmax != other.zmax

    def __eq__(self, other):
        return not self != other

    def __hash__(self):
        return hash(self.xmin) ^ hash(self.xmax)

    def __and__(self, other):
        return Cube(
            max(self.xmin, other.xmin),
            min(self.xmax, other.xmax),
            max(self.ymin, other.ymin),
            min(self.ymax, other.ymax),
            max(self.zmin, other.zmin),
            min(self.zmax, other.zmax),
        )

    def __contains__(self, other):
        return other.xmin >= self.xmin and other.xmax <= self.xmax \
           and other.ymin >= self.ymin and other.ymax <= self.ymax \
           and other.zmin >= self.zmin and other.zmax <= self.zmax

    def __len__(self):
        if self.xmax < self.xmin:
            return 0
        if self.ymax < self.ymin:
            return 0
        if self.zmax < self.zmin:
            return 0
        return (self.xmax + 1 - self.xmin) * (self.ymax + 1 - self.ymin) * (self.zmax + 1 - self.zmin)

    def disable(self, subcube):
        """
        Disable a subcube in the cube, then yield all the subcubes that are gained.
        This will split a cube into at most 27 subcubes
        It assumes the passed cube is indeed a subcube of this cube (uncomment line below for debug check)
        """
        # assert subcube in self

        for xrange in [(self.xmin, subcube.xmin - 1), (subcube.xmin, subcube.xmax), (subcube.xmax + 1, self.xmax)]:
            for yrange in [(self.ymin, subcube.ymin - 1), (subcube.ymin, subcube.ymax), (subcube.ymax + 1, self.ymax)]:
                for zrange in [(self.zmin, subcube.zmin - 1), (subcube.zmin, subcube.zmax), (subcube.zmax + 1, self.zmax)]:
                    cube = Cube(*xrange, *yrange, *zrange)
                    if len(cube):
                        yield cube


INPUT_REGEX = re.compile(r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$")
sequence = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        [state, *cube] = re.match(INPUT_REGEX, line.strip()).groups()
        sequence.append((state, Cube(*(int(coord) for coord in cube))))


for bounded in [True, False]:
    # keep track of cuboid regions that are on
    on_cubes = set()

    for state, cube in sequence:
        # bound input for part 1
        if bounded:
            _cube = cube & Cube(-50, 50, -50, 50, -50, 50)
            if not len(_cube):
                continue
        else:
            _cube = cube

        # split up all enabled cuboids with the intersection of the new cube
        # then add all subcubes that are not the intersection
        new_on = set()
        for on_cube in on_cubes:
            intersection = on_cube & _cube

            # empty intersection -> add original cube (nothing disabled)
            if not len(intersection):
                new_on.add(on_cube)
                continue

            for subcube in on_cube.disable(intersection):
                if subcube != intersection:
                    new_on.add(subcube)

        on_cubes = new_on

        # if we wanted to disable the cube we are done,
        # otherwise, add the new cube to the enabled regions
        if state == "on":
            on_cubes.add(_cube)

    print(sum(len(cube) for cube in on_cubes))