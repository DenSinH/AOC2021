from collections import defaultdict
import heapq


with open("input.txt", "r") as f:
    f.readline()  # #############
    f.readline()  # #...........#
    top = f.readline().strip().replace("#", "")
    bottom = f.readline().strip().replace("#", "")


class Pos:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


class State:

    ENERGY = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }
    ROOM = {
        "A": 2,
        "B": 4,
        "C": 6,
        "D": 8,
    }
    ROOM_EXITS = set(ROOM.values())

    def __init__(self, A, B, C, D, energy=0):
        self.A = tuple(A)
        self.B = tuple(B)
        self.C = tuple(C)
        self.D = tuple(D)
        self.energy = energy

    def pod_heuristic(self, pod, ptype):
        if pod.y == 2:
            if pod.x == State.ROOM[ptype]:
                return 0
            else:
                spot_taken = self.spot_taken(Pos(pod.x, 1))
                if spot_taken:
                    return 2 * State.ENERGY[spot_taken] + (abs(State.ROOM[ptype] - pod.x) + 4) * State.ENERGY[ptype]
                else:
                    return (abs(State.ROOM[ptype] - pod.x) + 4) * State.ENERGY[ptype]
        elif pod.y == 1:
            if pod.x == State.ROOM[ptype]:
                spot_taken = self.spot_taken(Pos(pod.x, 2))
                if spot_taken:
                    return 2 * State.ENERGY[spot_taken] + (abs(State.ROOM[ptype] - pod.x) + 4) * State.ENERGY[ptype]
                else:
                    return 0
            else:
                return (abs(State.ROOM[ptype] - pod.x) + 3) * State.ENERGY[ptype]
        return (abs(State.ROOM[ptype] - pod.x) + 2) * State.ENERGY[ptype]

    def heuristic(self):
        return self.energy \
               + sum(self.pod_heuristic(a, "A") for a in self.A) \
               + sum(self.pod_heuristic(b, "B") for b in self.B) \
               + sum(self.pod_heuristic(c, "C") for c in self.C) \
               + sum(self.pod_heuristic(d, "D") for d in self.D)

    def __eq__(self, other):
        return self.A == other.A and self.B == other.B and self.C == other.C and self.D == other.D

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __hash__(self):
        return hash(self.A) ^ hash(self.B) ^ hash(self.C) ^ hash(self.D)

    def __str__(self):
        field = "#############\n"
        field += "#" + "".join(self.spot_taken(Pos(x, 0)) or "." for x in range(11)) + "#\n"
        field += "###" + "#".join(self.spot_taken(Pos(State.ROOM[ptype], 1)) or "." for ptype in "ABCD") + "###\n"
        field += "  #" + "#".join(self.spot_taken(Pos(State.ROOM[ptype], 2)) or "." for ptype in "ABCD") + "#\n"
        field += "  #########"
        return field

    def __repr__(self):
        return str(self)

    def is_done(self):
        return {pos.y for pos in self.A} == {1, 2} \
           and {pos.y for pos in self.B} == {1, 2} \
           and {pos.y for pos in self.C} == {1, 2} \
           and {pos.y for pos in self.D} == {1, 2}

    def spot_taken(self, pos):
        if pos in self.A:
            return "A"
        elif pos in self.B:
            return "B"
        elif pos in self.C:
            return "C"
        elif pos in self.D:
            return "D"
        return None

    def move_pod(self, pod, ptype):
        if pod.y == 2:
            if pod.x != State.ROOM[ptype]:
                if not self.spot_taken(Pos(pod.x, 1)):
                    yield Pos(pod.x, 1), State.ENERGY[ptype]
        elif pod.y == 1:
            # move back into room
            if pod.x == State.ROOM[ptype]:
                if not self.spot_taken(Pos(pod.x, 2)):
                    yield Pos(pod.x, 2), State.ENERGY[ptype]

            # move out of room if we are not in the right room
            # or if there is a wrong pod in the back of our room
            if pod.x != State.ROOM[ptype] or self.spot_taken(Pos(pod.x, 2)) != ptype:
                for dx in range(1, pod.x + 1):
                    if self.spot_taken(Pos(pod.x - dx, 0)):
                        break
                    if pod.x - dx not in State.ROOM_EXITS:
                        yield Pos(pod.x - dx, 0), (1 + dx) * State.ENERGY[ptype]
                for dx in range(1, 1 + 10 - pod.x):
                    if self.spot_taken(Pos(pod.x + dx, 0)):
                        break
                    if pod.x + dx not in State.ROOM_EXITS:
                        yield Pos(pod.x + dx, 0), (1 + dx) * State.ENERGY[ptype]
        elif pod.y == 0:
            # move back into room if allowed
            # pods cannot stand in front of rooms anyway
            for x in range(min(pod.x, State.ROOM[ptype]) + 1, max(pod.x, State.ROOM[ptype])):
                if self.spot_taken(Pos(x, 0)):
                    return

            # cannot move into room
            if self.spot_taken(Pos(State.ROOM[ptype], 1)):
                return

            # pod in room of wrong type
            if (self.spot_taken(Pos(State.ROOM[ptype], 2)) or ptype) != ptype:
                return
            yield Pos(State.ROOM[ptype], 1), (abs(pod.x - State.ROOM[ptype]) + 1) * State.ENERGY[ptype]

    def moves(self):
        for pod, energy in self.move_pod(self.A[0], "A"):
            yield State((pod, self.A[1]), self.B, self.C, self.D, self.energy + energy)
        for pod, energy in self.move_pod(self.A[1], "A"):
            yield State((self.A[0], pod), self.B, self.C, self.D, self.energy + energy)
        for pod, energy in self.move_pod(self.B[0], "B"):
            yield State(self.A, (pod, self.B[1]), self.C, self.D, self.energy + energy)
        for pod, energy in self.move_pod(self.B[1], "B"):
            yield State(self.A, (self.B[0], pod), self.C, self.D, self.energy + energy)
        for pod, energy in self.move_pod(self.C[0], "C"):
            yield State(self.A, self.B, (pod, self.C[1]), self.D, self.energy + energy)
        for pod, energy in self.move_pod(self.C[1], "C"):
            yield State(self.A, self.B, (self.C[0], pod), self.D, self.energy + energy)
        for pod, energy in self.move_pod(self.D[0], "D"):
            yield State(self.A, self.B, self.C, (pod, self.D[1]), self.energy + energy)
        for pod, energy in self.move_pod(self.D[1], "D"):
            yield State(self.A, self.B, self.C, (self.D[0], pod), self.energy + energy)


state = defaultdict(list)
for pod, room in zip(top, "ABCD"):
    state[pod].append(Pos(State.ROOM[room], 1))
for pod, room in zip(bottom, "ABCD"):
    state[pod].append(Pos(State.ROOM[room], 2))
start = State(**dict(state.items()))

min_energy = float("inf")
states = {start: start}
todo = [(0, start)]

while todo:
    print(len(todo), min_energy)
    _, current = heapq.heappop(todo)
    if current.energy > min_energy:
        continue

    for state in current.moves():
        if state.is_done():
            min_energy = min(min_energy, state.energy)
            print(min_energy)
        else:
            if state in states:
                if state.energy >= states[state].energy:
                    continue
            states[state] = state
            heapq.heappush(todo, (state.heuristic(), state))

print(min_energy)