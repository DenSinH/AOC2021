with open("input.txt", "r") as f:
    program = [tuple(line.strip().split(" ")) for line in f.readlines()]

var = {}
advprog = "x = 0\ny = 0\nz = 0\nw = 0\n"


class Expr:

    def __init__(self, expr):
        self.expr = expr
        self.deps = set()

curr = {}
iszero = set()

for op, *args in program:
    assert op == "inp" or args[0] != args[1]

    if op == "div" and args[1] == "1":
        continue

    # flush expressions
    to_remove = []
    for other, expr in curr.items():
        if args[0] in expr.deps:
            advprog += f"{other} = {expr.expr}\n"
            to_remove.append(other)
    for other in to_remove:
        curr.pop(other)

    if (op == "mul" and args[1] == "0") or op == "inp":
        if args[0] in curr:
            advprog += f"{args[0]} = {curr[args[0]].expr}\n"
            curr.pop(args[0])
        if op == "inp":
            while curr:
                var = min(curr.keys())
                advprog += f"{var} = {curr.pop(var).expr}\n"
            advprog += f"{args[0]} = readinput()\n"
        else:
            iszero.add(args[0])
    elif args[0] not in curr:
        if args[0] not in iszero:
            curr[args[0]] = Expr({
                "add": lambda a, b: f"({a} + {b})",
                "mul": lambda a, b: f"({a} * {b})",
                "div": lambda a, b: f"({a} // {b})",
                "mod": lambda a, b: f"({a} % {b})",
                "eql": lambda a, b: f"int({a} == {b})" if b != "0" else f"int(not {a})"
            }[op](*args))
            curr[args[0]].deps.add(args[1])
        else:
            curr[args[0]] = Expr({
                "add": lambda a, b: f"{b}",
                "mul": lambda a, b: f"0",
                "div": lambda a, b: f"0",
                "mod": lambda a, b: f"0",
                "eql": lambda a, b: f"int(not {b})"
            }[op](*args))
            if op in {"add", "eql"}:
                curr[args[0]].deps.add(args[1])
        iszero.discard(args[0])
    else:
        curr[args[0]].expr = {
            "add": lambda expr, a, b: f"({expr} + {b})",
            "mul": lambda expr, a, b: f"({expr} * {b})",
            "div": lambda expr, a, b: f"({expr} // {b})",
            "mod": lambda expr, a, b: f"({expr} % {b})",
            "eql": lambda expr, a, b: f"int({expr} == {b})" if b != "0" else f"int(not {expr})"
        }[op](curr[args[0]].expr, *args)
        curr[args[0]].deps.add(args[1])

    if args[0] in curr:
        for var in curr[args[0]].deps:
            if var in curr:
                advprog += f"{var} = {curr[var].expr}\n"
                curr.pop(var)

    for var, expr in curr.items():
        assert var not in expr.deps

for var, expr in curr.items():
    advprog += f"{var} = {expr.expr}\n"


def do_advprog(inp):
    i = 0
    def readinput():
        nonlocal i
        val = inp[i]
        i += 1
        return int(val)

    exec(advprog)
    return z


def do_decompiled(inp):
    Z = 0
    fuzz_vals = [13, 11, 15, -6, 15, -8, -4, 15, 10, 11, -11,  0, -8, -7]
    add_vals  = [ 3, 12,  9, 12,  2,  1,  1, 13,  1,  6,   2, 11, 10,  3]
    do_div    = [ 0,  0,  0,  1,  0,  1,  1,  0,  0,  0,   1,  1,  1,  1]

    for char, fuzz, add, div in zip(inp, fuzz_vals, add_vals, do_div):
        if int(char) != ((Z % 26) + fuzz):
            if div:
                Z //= 26
            Z *= 26
            Z += int(char) + add
        else:
            if div:
                Z //= 26
    return Z


"""
note: char + add < 26 always

basically: Z is a string buffer
div: go back one in buffer

for every digit:
    if div:
        pop buffer

    if the last digit + fuzz == digit:
        new character = digit + offset
"""


def do_buf(inp):
    fuzz_vals = [13, 11, 15, -6, 15, -8, -4, 15, 10, 11, -11,  0, -8, -7]
    add_vals  = [ 3, 12,  9, 12,  2,  1,  1, 13,  1,  6,   2, 11, 10,  3]
    do_pop    = [ 0,  0,  0,  1,  0,  1,  1,  0,  0,  0,   1,  1,  1,  1]

    buf = []
    for char, fuzz, add, pop in zip(inp, fuzz_vals, add_vals, do_pop):
        last_char = buf[-1] if buf else 0
        if pop:
            buf = buf[:-1]
        if int(char) != (last_char + fuzz):
            buf.append(int(char) + add)

    num = 0
    for char in buf:
        num *= 26
        num += char
    return num


"""
the result will only be 0 if the buffer is empty at the end
we pop 7 times, so we can only push 7 times as well

there are also only 7 times where int(char) == ((Z % 26) + fuzz) can have a solution
this is only when fuzz < 10
In this case, we must have
    last digit + fuzz < 10 ==> last_digit < 10 - fuzz
    
coincidentally, fuzz < 10 if and only if pop == 1

so every time we pop a value, we also want to make sure we are not pushing a value
this makes it so we have to sort of "fold" the values with pop == 0 and pop == 1
I.e, consider
fuzz_vals = [13, 11, 15, -6, 15, -8, -4, 15, 10, 11, -11,  0, -8, -7]
add_vals  = [ 3, 12,  9, 12,  2,  1,  1, 13,  1,  6,   2, 11, 10,  3]
do_pop    = [ 0,  0,  0,  1,  0,  1,  1,  0,  0,  0,   1,  1,  1,  1]

notice how 
     11, -11,
      6,   2,
      0,   1,
has 0, 1 next to each other for pop, so we need to make sure that 
      v0 + 6  + -11 = v0 - 5 == v1
for v0, v1 input values from left to right
for part 1 we want to maximize this, for part 2 we want to minimize this
so for part 1: v0 = 9, v1 = 4
and for part 2: v0 = 6, v1 = 1

so we have solved these 2 columns, then for the next column (where we also pop a value), the last value in the 
buffer is the one corresponding to the previous column (where we dont pop a value), I.e. we do the same thing for
    10, (11, -11,)  0,
     1, ( 6,   2,) 11,
     0, ( 0,   1,)  1,
to find that
    v0 + 1 + 0 = v1  ==> v0 = 8, v1 = 9 for part 1, v0 = 1, v1 = 2 for part 2
etc. with the correspondences

fuzz_vals = [13, 11, 15, -6, 15, -8, -4, 15, 10, 11, -11,  0, -8, -7]
add_vals  = [ 3, 12,  9, 12,  2,  1,  1, 13,  1,  6,   2, 11, 10,  3]
do_pop    = [ 0,  0,  0,  1,  0,  1,  1,  0,  0,  0,   1,  1,  1,  1]
              |   |   +---+   +---+   |   |   |   +----+   |   |   |
              |   +-------------------+   |   +------------+   |   |
              |                           +--------------------+   |
              +----------------------------------------------------+
"""

fuzz_vals = [13, 11, 15, -6, 15, -8, -4, 15, 10, 11, -11,  0, -8, -7]
add_vals  = [ 3, 12,  9, 12,  2,  1,  1, 13,  1,  6,   2, 11, 10,  3]
do_pop    = [ 0,  0,  0,  1,  0,  1,  1,  0,  0,  0,   1,  1,  1,  1]

part1     = [ 9,  1,  6,  9,  9,  3,  9,  4,  8,  9,   4,  9,  9,  5]
part2     = [ 5,  1,  1,  4,  7,  1,  9,  1,  1,  6,   1,  2,  6,  1]

for part in (part1, part2):
    inp = "".join(str(d) for d in part)
    print(inp)
    assert do_buf(inp) == 0
