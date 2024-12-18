from collections import defaultdict
from heapq import heappop, heappush
from functools import cache
from copy import deepcopy


def read_input(filename):
    corrupted = []
    with open(filename) as f:
        for line in f:
            corrupted.append(C(*map(int, line.strip().split(","))))

    return corrupted


class C:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return C(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return C(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)


@cache
def get_all_neighbours(max_x, max_y):
    deltas = (C(0, 1), C(1, 0), C(0, -1), C(-1, 0))
    neighbours = defaultdict(dict)

    for x in range(max_x):
        for y in range(max_y):
            cur = C(x, y)
            for delta in deltas:
                new_pos = cur + delta
                if (
                    new_pos.x >= 0
                    and new_pos.x < max_x
                    and new_pos.y >= 0
                    and new_pos.y < max_y
                ):
                    neighbours[cur][new_pos] = 1
    return neighbours


def get_neighbours(max_x, max_y, corrupted):
    neighbours = deepcopy(get_all_neighbours(max_x, max_y))

    corrupted_set = set(corrupted)

    for node in neighbours:
        for neighbour in neighbours[node].keys():
            if neighbour in corrupted_set:
                neighbours[node][neighbour] = float("inf")

    return neighbours


def dijkstra_heap(neighbours, start, end):
    dist = {point: float("inf") for point in neighbours}
    prev = {}
    dist[start] = 0

    # Priority queue with (distance, vertex)
    Q = [(0, start)]
    seen = set()

    while Q:
        d, u = heappop(Q)

        if u == end:
            return dist, prev

        if u in seen or d > dist[u]:
            continue
        seen.add(u)

        for v, weight in neighbours[u].items():
            if v not in seen:
                alt = d + weight
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u  # Add the new optimal path
                    heappush(Q, (alt, v))

    return dist, prev


def get_path(end, prev):
    path = []
    while end:
        path.append(end)
        end = prev[end]
    return path


def print_grid(max_x, max_y, corrupted, paths):
    for y in range(max_y):
        for x in range(max_x):
            if C(x, y) in corrupted:
                print("#", end="")
            elif any(C(x, y) in path for path in paths):
                print("O", end="")
            else:
                print(".", end="")
        print()


def one(corrupted, size_x, size_y, n_bytes):
    neighbours = get_neighbours(size_x, size_y, corrupted[:n_bytes])
    start = C(0, 0)
    end = C(size_x - 1, size_y - 1)
    cost, _ = dijkstra_heap(neighbours, start, end)

    return cost[end]


def two(corrupted, size_x, size_y):
    min_bytes = 0
    max_bytes = len(corrupted)

    start = C(0, 0)
    end = C(size_x - 1, size_y - 1)

    while min_bytes < max_bytes:
        mid = (min_bytes + max_bytes) // 2
        neighbours = get_neighbours(size_x, size_y, corrupted[:mid])
        cost, _ = dijkstra_heap(neighbours, start, end)

        # print(min_bytes, mid, max_bytes, cost.get(end, float("inf")))
        if cost.get(end, float("inf")) == float("inf"):
            max_bytes = mid
        else:
            min_bytes = mid + 1

    neighbours = get_neighbours(size_x, size_y, corrupted)
    cost, _ = dijkstra_heap(neighbours, start, end)

    return f"{corrupted[mid].x},{corrupted[mid].y}"


def main():
    test_corrupted = read_input("test.txt")
    assert 22 == one(test_corrupted, 7, 7, 12)

    corrupted = read_input("input.txt")
    print(one(corrupted, 71, 71, 1024))

    assert two(test_corrupted, 7, 7) == "6,1"

    print(two(corrupted, 71, 71))


if __name__ == "__main__":
    main()
