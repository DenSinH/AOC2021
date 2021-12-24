from collections import defaultdict
import numpy as np
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
        return f"Pos({self.x}, {self.y})"


class State:

    ENERGY = [
        None,
        1,
        10,
        100,
        1000,
    ]
    ROOM = [
        None,
        2,
        4,
        6,
        8,
    ]
    ROOM_EXITS = set(ROOM[1:])
    TILE = ".ABCD"

    def __init__(self, field, energy=0, num_pods=2):
        self.field: np.array = field
        self.num_pods = num_pods
        self.energy = energy
        self._heuristic = None

    def pod_heuristic(self, pod, ptype):
        if pod.x != State.ROOM[ptype]:
            if pod.y == 0:
                return State.ENERGY[ptype]
            return abs(State.ROOM[ptype] - pod.x + 2 + pod.y) * State.ENERGY[ptype]
        return 0

    def heuristic(self):
        if self._heuristic is None:
            self._heuristic = self.energy + sum(self.pod_heuristic(pod, self.field[pod.x, pod.y]) for pod in self.pods())
        return self._heuristic

    def __eq__(self, other):
        return np.all(self.field == other.field)

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __hash__(self):
        return hash(self.field.tobytes())

    def __str__(self):
        field = "#############\n"
        field += "#" + "".join(State.TILE[self.spot_taken(Pos(x, 0))] for x in range(11)) + "#\n"
        field += "###" + "#".join(State.TILE[self.spot_taken(Pos(State.ROOM[ptype], 1))] for ptype in [1, 2, 3, 4]) + "###\n"
        field += "  #" + "#".join(State.TILE[self.spot_taken(Pos(State.ROOM[ptype], 2))] for ptype in [1, 2, 3, 4]) + "#\n"
        field += "  #########"
        return field

    def __repr__(self):
        return str(self)

    def is_done(self):
        return all(pod.x == State.ROOM[self.field[pod.x, pod.y]] for pod in self.pods())

    def spot_taken(self, pos):
        return self.field[pos.x, pos.y]

    def move_pod(self, pod, ptype):
        if pod.y >= 1:
            # move out of room if we are not in the right room
            # or if there is a wrong pod in the back of our room
            if pod.x != State.ROOM[ptype] or \
                    any((self.spot_taken(Pos(pod.x, pod.y + dy)) or ptype) != ptype for dy in range(1, 1 + self.num_pods - pod.y)):
                # can't go out of room if any spot is taken
                if any(self.spot_taken(Pos(pod.x, y)) for y in range(1, pod.y)):
                    return
                for dx in range(1, pod.x + 1):
                    if self.spot_taken(Pos(pod.x - dx, 0)):
                        break
                    if pod.x - dx not in State.ROOM_EXITS:
                        yield Pos(pod.x - dx, 0), (pod.y + dx) * State.ENERGY[ptype]
                for dx in range(1, 1 + 10 - pod.x):
                    if self.spot_taken(Pos(pod.x + dx, 0)):
                        break
                    if pod.x + dx not in State.ROOM_EXITS:
                        yield Pos(pod.x + dx, 0), (pod.y + dx) * State.ENERGY[ptype]
        else:
            # move back into room if allowed
            # pods cannot stand in front of rooms anyway
            for x in range(min(pod.x, State.ROOM[ptype]) + 1, max(pod.x, State.ROOM[ptype])):
                if self.spot_taken(Pos(x, 0)):
                    return

            # pod in room of wrong type
            if any((self.spot_taken(Pos(State.ROOM[ptype], y)) or ptype) != ptype for y in range(1, self.num_pods + 1)):
                return

            # check how deep we can move into the room
            for y in range(1, self.num_pods + 1):
                if self.spot_taken(Pos(State.ROOM[ptype], y)):
                    break
            else:
                y = self.num_pods + 1
            if y > 1:
                yield Pos(State.ROOM[ptype], y - 1), (abs(pod.x - State.ROOM[ptype]) + y - 1) * State.ENERGY[ptype]

    def pods(self):
        for x, y in zip(*np.nonzero(self.field)):
            yield Pos(x, y)

    def moves(self):
        for pod in self.pods():
            for nxt, energy in self.move_pod(pod, self.field[pod.x, pod.y]):
                new_field = np.array(self.field)
                new_field[pod.x, pod.y] = 0
                new_field[nxt.x, nxt.y] = self.field[pod.x, pod.y]
                yield State(new_field, self.energy + energy, self.num_pods)


def solve(part):
    state = defaultdict(list)
    for pod, room in zip(top, [1, 2, 3, 4]):
        state[pod].append(Pos(State.ROOM[room], 1))
    for pod, room in zip(bottom, [1, 2, 3, 4]):
        state[pod].append(Pos(State.ROOM[room], 2 if part == 1 else 4))
    if part == 2:
        state["A"].append(Pos(State.ROOM[4], 2))
        state["A"].append(Pos(State.ROOM[3], 3))
        state["B"].append(Pos(State.ROOM[2], 3))
        state["B"].append(Pos(State.ROOM[3], 2))
        state["C"].append(Pos(State.ROOM[4], 3))
        state["C"].append(Pos(State.ROOM[2], 2))
        state["D"].append(Pos(State.ROOM[1], 2))
        state["D"].append(Pos(State.ROOM[1], 3))

    grid = np.zeros((11, 1 + 2 * part), dtype=np.int32)
    for ptype, pods in state.items():
        for pod in pods:
            grid[pod.x, pod.y] = 1 + "ABCD".index(ptype)

    start = State(grid, num_pods=2 * part)

    states = {start: start}
    todo = [(0, start)]

    while todo:
        h, current = heapq.heappop(todo)
        if current.energy > states[current].energy:
            continue

        for state in current.moves():
            if state.is_done():
                return state.energy
            else:
                if state in states:
                    if state.energy >= states[state].energy:
                        continue
                states[state] = state
                heapq.heappush(todo, (state.heuristic(), state))

    return float("inf")


print(solve(1))
print(solve(2))