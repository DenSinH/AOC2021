with open("input.txt", "r") as f:
    input = [line.strip() for line in f.readlines()]

match = { ")": "(", "]": "[", "}": "{", ">": "<" }
score1 = { ")": 3, "]": 57, "}": 1197, ">": 25137 }
score2 = { "(": 1, "[": 2, "{": 3, "<": 4 }
part1 = 0
part2 = []
for line in input:
    stack = []
    for bracket in line:
        if bracket in match:
            if match[bracket] != stack.pop():
                part1 += score1[bracket]
                break
        else:
            stack.append(bracket)
    else:
        part2.append(0)
        while stack:
            part2[-1] = (part2[-1] * 5) + score2[stack.pop()]

print(part1)
print(sorted(part2)[(len(part2) - 1) >> 1])
