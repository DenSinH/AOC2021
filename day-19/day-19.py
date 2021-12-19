import itertools as it
from collections import Counter


xflip = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, z, -y),
]
yflip = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-z, y, x),
]
zflip = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-y, x, z),
]


def permute(point, orientation):
    return orientation[0](*(orientation[1](*(orientation[2](*point)))))


# for generating the permutations:
for permuted in {permute((1, 2, 3), orientation) for orientation in it.product(xflip, yflip, zflip)}:
    print(f"lambda x, y, z: {permuted},".replace("1", "x").replace("2", "y").replace("3", "z"))


# outputs:
orientations = [
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (-x, -z, -y),
]


def translate(point, offset):
    return point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]


class Transformation:

    def __init__(self, orientation, translation):
        self.orientation = orientation
        self.translation = translation

    def __eq__(self, other):
        return self.translation == other.translation and self.orientation == other.orientation

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.translation)


scanners = []
with open("input.txt", "r") as f:
    while f.readline():  # --- scanner x ---
        scanners.append(set())
        while line := f.readline().strip():  # ends with blank line
            scanners[-1].add(eval(f"({line})"))

scanner0 = scanners.pop(0)
beacons = set(scanner0)


def scanner_correspondence(scanner):
    transforms = Counter()
    for orientation in orientations:
        for beacon in scanner:
            permuted = orientation(*beacon)
            for corresponding in beacons:
                translation = (
                    corresponding[0] - permuted[0],
                    corresponding[1] - permuted[1],
                    corresponding[2] - permuted[2]
                )
                transforms[Transformation(orientation, translation)] += 1

    most_common = transforms.most_common(1)[0][0]
    scanner_ = {translate(most_common.orientation(*b), most_common.translation) for b in scanner}

    if len(scanner_ & beacons) >= 12:
        return most_common.translation, scanner_
    return None, None


positions = {}
while len(positions) != len(scanners):
    for i, scanner in enumerate(scanners):
        if i + 1 in positions:
            continue
        print("trying scanner", i + 1)

        translation, correspondence = scanner_correspondence(scanner)
        if correspondence is not None:
            positions[i + 1] = translation
            beacons |= correspondence

    print(positions)
    print(len(beacons))

print("part 1", len(beacons))

positions[0] = (0, 0, 0)
max_dist = 0
for i in range(len(scanners) + 1):
    for j in range(i, len(scanners) + 1):
        max_dist = max(max_dist, sum(abs(positions[i][c] - positions[j][c]) for c in range(3)))
print("part 2", max_dist)