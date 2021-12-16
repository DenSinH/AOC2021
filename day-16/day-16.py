from functools import reduce


class Literal:

    def __init__(self, version, number):
        self.version = version
        self.number = number

    def __str__(self):
        return str(self.number)

    def version_sum(self):
        return self.version

    def eval(self):
        return self.number


class Operator:

    def __init__(self, version, tid, children):
        self.version = version
        self.tid = tid
        self.children = children

    def __str__(self):
        return f"[{self.tid}, {self.version}]({'|'.join((str(child) for child in self.children))})"

    def version_sum(self):
        return self.version + sum(child.version_sum() for child in self.children)

    def eval(self):
        """
        We abuse the order of evaluation in python:

        Order of Evaluation
        In Python, the left operand is always evaluated before the right operand.
        That also applies to function arguments.
        """
        op = [
            sum,
            lambda c: reduce(lambda x, y: x * y, c, 1),
            min,
            max,
            None,
            lambda c: int(next(c) > next(c)),
            lambda c: int(next(c) < next(c)),
            lambda c: int(next(c) == next(c)),
        ][self.tid]
        return op(child.eval() for child in self.children)


def decode_message(message, is_hex=False):
    if is_hex:
        message = format(int(message, 16), f'0>{4 * len(message)}b')

    return decode_packet(message, 0)[0]


def decode_packet(message, index):
    version = int(message[index:index + 3], 2)
    index += 3
    tid = int(message[index:index + 3], 2)
    index += 3
    if tid == 4:
        number = 0
        while True:
            has_next = message[index] == "1"
            number <<= 4
            number |= int(message[index + 1:index + 5], 2)
            index += 5
            if not has_next:
                break
        return Literal(version, number), index
    else:
        children = []
        length_id = message[index] == "1"
        index += 1
        if length_id:
            # 11 bits length
            length = int(message[index:index + 11], 2)
            index += 11
            for c in range(length):
                child, index = decode_packet(message, index)
                children.append(child)
        else:
            # 15 bits length
            length = int(message[index:index + 15], 2)
            index += 15
            length_found = 0
            while length_found < length:
                child, next_index = decode_packet(message, index)
                length_found += next_index - index
                index = next_index
                children.append(child)
        return Operator(version, tid, children), index


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        message = f.readline().strip()

    decoded = decode_message(message, is_hex=True)
    print(decoded.version_sum())
    print(decoded.eval())