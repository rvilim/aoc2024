from heapq import heappop, heappush
from collections import defaultdict
import copy
from itertools import combinations
from functools import cache


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


def get_input(filename):
    maze = {}

    with open(filename) as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                if char == "S":
                    maze[C(x, y)] = "."
                    start = C(x, y)
                elif char == "E":
                    maze[C(x, y)] = "."
                    end = C(x, y)
                else:
                    maze[C(x, y)] = char
    return start, end, maze


def get_bounds(maze):
    max_y = 0
    max_x = 0
    for pos in maze.keys():
        max_x, max_y = max(max_x, pos.x), max(max_y, pos.y)
    return max_x, max_y


def parse_neighbors(maze):
    max_x, max_y = get_bounds(maze)
    neighbours = defaultdict(dict)
    deltas = (C(-1, 0), C(1, 0), C(0, -1), C(0, 1))

    for cur, val in maze.items():
        for delta in deltas:
            new_pos = cur + delta
            if (
                new_pos.x >= 0
                and new_pos.x < max_x
                and new_pos.y >= 0
                and new_pos.y < max_y
                and maze[new_pos] == "."
            ):
                neighbours[cur][new_pos] = 1.0
            else:
                neighbours[cur][new_pos] = float("inf")
    return neighbours


def print_maze(maze, start, end, path=[]):
    path_set = set(path)
    max_x, max_y = get_bounds(maze)

    for y in range(max_y):
        for x in range(max_x):
            pos = C(x, y)
            if pos in path_set:
                print("O", end="")
            elif pos == start:
                print("S", end="")
            elif pos == end:
                print("E", end="")
            elif maze[pos] in ("#", ".", "?"):
                print(maze[pos], end="")
        print("")


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
        try:
            end = prev[end]
        except KeyError:
            return path[::-1]
    raise ValueError


def get_mazes(base_neighbours):
    cheat_deltas = (
        C(1, 0),
        C(0, 1),
    )  # only including positive deltas because we don't need to double run
    all_deltas = (C(1, 0), C(0, 1), C(-1, 0), C(0, -1))

    max_x, max_y = get_bounds(base_neighbours)

    for cheat_one in base_neighbours.keys():
        neighbours = copy.deepcopy(base_neighbours)

        if (
            cheat_one.x == 0
            or cheat_one.x == max_x
            or cheat_one.y == 0
            or cheat_one.y == max_y
        ):
            continue

        for delta in cheat_deltas:
            cheat_two = cheat_one + delta
            if (
                cheat_two.x == 0
                or cheat_two.x == max_x
                or cheat_two.y == 0
                or cheat_two.y == max_y
            ):
                continue

            for cheat in (cheat_one, cheat_two):
                for delta in all_deltas:
                    neighbours[cheat + delta][cheat] = 1

            yield neighbours, cheat_one


def manhattan(pt1, pt2):
    dx = pt2.x - pt1.x
    dy = pt2.y - pt1.y
    return (dx if dx > 0 else -dx) + (dy if dy > 0 else -dy)


def solve(start, end, maze, cheat_length):
    import cProfile
    import pstats

    cheats = defaultdict(int)
    neighbours = parse_neighbors(maze)
    dist, prev = dijkstra_heap(neighbours, start, end)
    path = get_path(end, prev)

    for pt1, pt2 in combinations(path, 2):
        # This is just an inlined and sped up manhattan distance. the weird abs_dx calculation is faster than abs()
        # We also just check the x coord before calculating the y coord

        cheat_dist = abs(pt2.x - pt1.x)
        if cheat_dist > cheat_length:
            continue

        cheat_dist += abs(pt2.y - pt1.y)

        if cheat_dist <= cheat_length:
            cheats[int((dist[pt2] - dist[pt1]) - cheat_dist)] += 1

    result = sum(
        cheats[key] for key in cheats.keys() if key >= 100 and cheats[key] != 0
    )

    return result


def one(start, end, maze):
    return solve(start, end, maze, 2)


def two(start, end, maze):
    return solve(start, end, maze, 20)


def main():
    start, end, maze = get_input("test.txt")
    assert one(start, end, maze) == 0

    start, end, maze = get_input("input.txt")
    print(one(start, end, maze))
    print(two(start, end, maze))


if __name__ == "__main__":
    main()
