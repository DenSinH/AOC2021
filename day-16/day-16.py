from math import prod


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
            prod,
            min,
            max,
            None,
            lambda c: int(next(c) > next(c)),
            lambda c: int(next(c) < next(c)),
            lambda c: int(next(c) == next(c)),
        ][self.tid]
        return op(child.eval() for child in self.children)


class Message:

    def __init__(self, msg, is_hex=True):
        if is_hex:
            self.msg = format(int(msg, 16), f'0>{4 * len(message)}b')
        else:
            self.msg = msg
        self.index = 0

    def fetch(self, amount):
        value = int(self.msg[self.index:self.index + amount], 2)
        self.index += amount
        return value

    def packet(self):
        version = self.fetch(3)
        tid = self.fetch(3)
        if tid == 4:
            number = 0
            while True:
                has_next = self.fetch(1)
                number <<= 4
                number |= self.fetch(4)
                if not has_next:
                    return Literal(version, number)
        else:
            children = []
            if self.fetch(1):
                # 11 bits length
                length = self.fetch(11)
                for c in range(length):
                    children.append(self.packet())
            else:
                # 15 bits length
                length = self.fetch(15)
                end = self.index + length
                while self.index < end:
                    children.append(self.packet())
            return Operator(version, tid, children)


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        message = f.readline().strip()

    decoded = Message(message, is_hex=True).packet()
    print(decoded.version_sum())
    print(decoded.eval())
