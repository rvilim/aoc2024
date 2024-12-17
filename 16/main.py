from collections import defaultdict
from heapq import heappop, heappush


class C:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return C(self.x + other.x, self.y + other.y)

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


DIRS = (C(0, 1), C(1, 0), C(0, -1), C(-1, 0))

ROTATE_COSTS = {
    C(0, 1): [(C(1, 0), 1000), (C(-1, 0), 1000)],
    C(1, 0): [(C(0, 1), 1000), (C(0, -1), 1000)],
    C(0, -1): [(C(-1, 0), 1000), (C(1, 0), 1000)],
    C(-1, 0): [(C(0, -1), 1000), (C(0, 1), 1000)],
}


def parse(filename):
    maze = {}
    neighbours = defaultdict(dict)

    with open(filename) as f:
        for y, line in enumerate(f):
            parts = line.strip()
            for x, char in enumerate(parts):
                maze[C(x, y)] = char

    start = None
    end = None

    for facing_dir in DIRS:
        for pos, char in maze.items():
            if char == "#":
                continue

            if maze.get(pos + facing_dir, "#") != "#":
                neighbours[(pos, facing_dir)][pos + facing_dir, facing_dir] = 1

            for rotate_dir, cost in ROTATE_COSTS[facing_dir]:
                # if maze.get(pos+rotate_dir, "#") != "#":
                neighbours[(pos, facing_dir)][pos, rotate_dir] = cost
            if char == "S":
                start = (pos, C(1, 0))
            elif char == "E":
                end = pos

    return maze, neighbours, start, end


def print_maze(maze, path):
    for y in range(int(max(m.y for m in maze.keys()))):
        for x in range(int(max(m.x for m in maze.keys()))):
            if C(x, y) in path:
                print("O", end="")
            else:
                print(maze.get(C(x, y), " "), end="")
        print()


def djikstra(neighbours, start, end):
    dist = {}
    prev = {}
    Q = set()

    for point in neighbours.keys():
        dist[point] = float("inf")
        prev[point] = []
        Q.add(point)
    dist[start] = 0

    while Q:
        u = min(Q, key=lambda x: dist[x])
        if u == end:
            return dist[u], prev[u]
        Q.remove(u)

        for v in neighbours[u]:
            if v not in Q:
                continue
            alt = dist[u] + neighbours[u][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v].append(u)
    raise Exception("No path found")


def dijkstra_heap(neighbours, start, end):
    dist = {}
    prev = defaultdict(list)

    # Initialize distances
    for point in neighbours.keys():
        dist[point] = float("inf")
        # prev[point] = None
    dist[start] = 0

    # Priority queue with (distance, vertex)
    Q = [(0, start)]
    seen = set()

    while Q:
        d, u = heappop(Q)

        if u in seen:
            continue
        seen.add(u)

        for v, weight in neighbours[u].items():
            if v in seen:
                continue

            alt = dist[u] + weight
            if alt < dist[v]:
                dist[v] = alt
                dist[v] = alt
                prev[v].clear()  # Clear previous paths
                prev[v].append(u)  # Add the new optimal path
                heappush(Q, (alt, v))
            elif alt == dist[v]:  # If we found an equal-length path
                prev[v].append(u)  # Add this path as an alternative

    return dist, prev


def one(neighbours, start, end):
    min_cost = float("inf")
    for dir in DIRS:
        e = (end, dir)
        cost, _ = dijkstra_heap(neighbours, start, e)
        if cost[e] < min_cost:
            min_cost = cost[e]

    return min_cost


def get_paths(cur, prev, visited=None):
    if visited is None:
        visited = set()

    # if we've already visited this node, stop to prevent cycles
    if cur in visited:
        return []

    # if there are no previous nodes, this must be the start
    if not prev[cur]:
        return [[cur]]

    paths = []
    visited.add(cur)

    for p in prev[cur]:
        for path in get_paths(p, prev, visited):
            paths.append(path + [cur])

    visited.remove(cur)
    return paths


def two(neighbours, start, end, maze):
    min_cost = float("inf")
    min_prev = None
    points = set()

    for dir in DIRS:
        e = (end, dir)
        cost, prev = dijkstra_heap(neighbours, start, e)
        if cost[e] < min_cost:
            min_cost = cost[e]
            min_prev = prev
            min_end = e

    paths = get_paths(min_end, min_prev)
    for path in paths:
        for point in path:
            points.add(point[0])

    return len(points)


def main():
    maze, neighbours, start, end = parse("test1.txt")
    assert 7036 == one(neighbours, start, end)

    maze, neighbours, start, end = parse("input.txt")
    print(one(neighbours, start, end))

    maze, neighbours, start, end = parse("test1.txt")
    assert 45 == two(neighbours, start, end, maze)

    maze, neighbours, start, end = parse("test2.txt")
    assert 64 == two(neighbours, start, end, maze)

    maze, neighbours, start, end = parse("input.txt")
    print(two(neighbours, start, end, maze))


if __name__ == "__main__":
    main()
