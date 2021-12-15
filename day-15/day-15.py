import numpy as np
import heapq


class PrioQueue:

    def __init__(self, key=lambda x: x):
        self.key = key
        self.heap = []
        self.finder = set()

    def try_remove(self, item):
        if item not in self.finder:
            return
        index = self.heap.index((self.key(item), item))
        self.heap[index] = self.heap[-1]
        self.heap.pop()
        heapq.heapify(self.heap)

    def push(self, item):
        self.finder.add(item)
        heapq.heappush(self.heap, (self.key(item), item))

    def pop(self):
        item = heapq.heappop(self.heap)[1]
        self.finder.remove(item)
        return item


with open("input.txt", "r") as f:
    grid = np.array([[int(n) for n in line.strip()] for line in f.readlines()], dtype=np.int32)


def solve(scale):
    # rough estimate for maximum possible distance
    dist = scale * 9 * grid.size * np.ones((scale * grid.shape[0], scale * grid.shape[1]), dtype=np.int32)
    dist[0, 0] = 0

    def heuristic(x, y):
        return dist[x, y] + abs(scale * grid.shape[0] - x) + abs(scale * grid.shape[1] - y)

    def risk(x, y):
        # lot of unnecessary calculation for scale = 1 but eh...
        r = grid[x % grid.shape[0], y % grid.shape[1]] + int(x / grid.shape[0]) + int(y / grid.shape[1])
        return ((r - 1) % 9) + 1

    points = PrioQueue(key=lambda point: heuristic(*point))
    points.push((0, 0))
    while points:
        x, y = points.pop()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if x + dx == scale * grid.shape[0] - 1 and y + dy == scale * grid.shape[1] - 1:
                return int(dist[x, y] + risk(x + dx, y + dy))

            if 0 <= x + dx < scale * grid.shape[0] and 0 <= y + dy < scale * grid.shape[1]:
                if dist[x, y] + risk(x + dx, y + dy) < dist[x + dx, y + dy]:
                    # key will change, so remove then change the key, then add again
                    points.try_remove((x + dx, y + dy))
                    dist[x + dx, y + dy] = dist[x, y] + risk(x + dx, y + dy)
                    points.push((x + dx, y + dy))


print(solve(1))
print(solve(5))
