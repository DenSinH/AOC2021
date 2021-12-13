connections = {}
with open("input.txt", "r") as f:
    for [start, end] in (line.strip().split("-") for line in f.readlines()):
        if end != "start":
            connections[start] = connections.get(start, []) + [end]
        if start != "start":
            connections[end] = connections.get(end, []) + [start]

part1 = set()
todo = {(conn,) for conn in connections["start"]}

while todo:
    current = todo.pop()
    end = current[-1]
    for cave in connections.get(end, []):
        if cave == "end":
            part1.add(current)
        elif cave.upper() == cave or cave not in current:
            todo.add((*current, cave))

part2 = set()
todo = {(True, (conn,)) for conn in connections["start"]}  # I know, bad practice

while todo:
    allow_double, current = todo.pop()
    end = current[-1]
    for cave in connections.get(end, []):
        if cave == "end":
            part2.add(current)
        elif cave.upper() == cave or cave not in current:
            todo.add((allow_double, (*current, cave)))
        elif current.count(cave) == 1 and allow_double:
            todo.add((False, (*current, cave)))

print(len(part1))
print(len(part2))