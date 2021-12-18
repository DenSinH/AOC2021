

def add(snailfish, left=None, right=None):
    # add recursively to one side (after explosion)
    if left is not None:
        if isinstance(snailfish[0], list):
            add(snailfish[0], left=left)
        else:
            snailfish[0] += left

    if right is not None:
        if isinstance(snailfish[1], list):
            add(snailfish[1], right=right)
        else:
            snailfish[1] += right


def explode(snailfish, layer=0):
    if layer == 4:
        if isinstance(snailfish, list):
            numbers = tuple(snailfish)

            # make reference empty
            snailfish.pop()
            snailfish.pop()
            return *numbers, True
    else:
        left = None
        right = None
        has_exploded = False

        # explode left then right
        if isinstance(snailfish[0], list):
            left, _right, _ = explode(snailfish[0], layer + 1)
            if _right is not None:
                # add right to nested snail, return left to outer snail
                if isinstance(snailfish[1], int):
                    snailfish[1] += _right
                else:
                    add(snailfish[1], left=_right)

            if not snailfish[0]:
                # fix empty lists
                snailfish[0] = 0
                has_exploded = True

        # same for right
        if isinstance(snailfish[1], list):
            _left, right, _ = explode(snailfish[1], layer + 1)
            if _left is not None:
                if isinstance(snailfish[0], int):
                    snailfish[0] += _left
                else:
                    add(snailfish[0], right=_left)
            if not snailfish[1]:
                snailfish[1] = 0
                has_exploded = True

        return left, right, has_exploded


def split(snailfish):
    # only split once (explosions might happen after)
    for i in [0, 1]:
        if isinstance(snailfish[i], list):
            if split(snailfish[i]):
                return True
        else:
            if snailfish[i] >= 10:
                snailfish[i] = [int(snailfish[i] / 2), int((snailfish[i] + 1) / 2)]
                return True
    return False


def reduce(snailfish):
    while True:
        # keep exploding
        while explode(snailfish)[-1]:
            pass
        # if we cannot split then we are done
        if not split(snailfish):
            return


def magnitude(snailfish):
    if isinstance(snailfish, list):
        return 3 * magnitude(snailfish[0]) + 2 * magnitude(snailfish[1])
    else:
        return snailfish


with open("input.txt", "r") as f:
    numbers = [line for line in f.readlines()]

# keep adding numbers from input
# do eval cause the input is nice and we don't have to mess with list references after that for part 2
number = eval(numbers[0])
reduce(number)
for line in numbers[1:]:
    number = [number, eval(line)]
    reduce(number)

print(magnitude(number))

# consider all pairs
highest = 0
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        number = [eval(numbers[i]), eval(numbers[j])]
        reduce(number)
        highest = max(highest, magnitude(number))

        number = [eval(numbers[j]), eval(numbers[i])]
        reduce(number)
        highest = max(highest, magnitude(number))

print(highest)