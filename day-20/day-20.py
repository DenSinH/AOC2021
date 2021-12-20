with open("input.txt", "r") as f:
    iea = [c == "#" for c in f.readline().strip()]
    assert len(iea) == 512
    f.readline()
    image = set()
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line.strip()):
            if c == "#":
                image.add((x, y))


def enhance(image, neg_image, outside_value):
    new = set()
    new_neg = set()

    for x, y in image:
        for dy in [-2, -1, 0, 1, 2]:
            for dx in [-2, -1, 0, 1, 2]:
                nx, ny = x + dx, y + dy

                if (nx, ny) in new or (nx, ny) in new_neg:
                    continue

                index = 0
                for ddy in [-1, 0, 1]:
                    for ddx in [-1, 0, 1]:
                        index <<= 1
                        index |= int(((nx + ddx, ny + ddy) in image) or (((nx + ddx, ny + ddy) not in neg_image) and outside_value))

                if iea[index]:
                    new.add((nx, ny))
                else:
                    new_neg.add((nx, ny))
    return new, new_neg, iea[-1 if outside_value else 0]


def print_image(image):
    xmin = min([x for x, y in image])
    xmax = max([x for x, y in image])
    ymin = min([y for x, y in image])
    ymax = max([y for x, y in image])
    for y in range(ymin, ymax + 1):
        print("".join("#" if (x, y) in image else " " for x in range(xmin, xmax + 1)))


enhanced = image
neg = set()
outside = False
for times in (2, 48):
    for i in range(times):
        enhanced, neg, outside = enhance(enhanced, neg, outside)
    print(len(enhanced))
