from collections import defaultdict
from itertools import combinations


def print_grid(antennae, antinodes, bounds):
    print(antinodes)
    print(antennae)
    max_x, max_y = bounds

    print("  ", end="")
    for x in range(max_x + 1):
        print(x, end="")
    print()
    for y in range(max_y + 1):
        print(f"{y} ", end="")
        for x in range(max_x + 1):
            coord_printed = False
            for char, coords in antennae.items():
                if (x, y) in coords:
                    print(char, end="")
                    coord_printed = True
                    break
            if not coord_printed:
                if (x, y) in antinodes:
                    print("#", end="")
                else:
                    print(".", end="")
        print()


def read_input(filename):
    antennae = defaultdict(list)

    with open(filename) as f:
        max_x, max_y = 0, 0
        for y, line in enumerate(f):
            max_y = y
            for x, c in enumerate(line.strip()):
                max_x = x
                if c != ".":
                    antennae[c].append((x, y))
    return antennae, (max_x, max_y)


def diff(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def scale(v, s):
    return (v[0] * s, v[1] * s)


def solve(antennae, bounds, resonant):
    antinodes = set()
    max_x, max_y = bounds

    if resonant:
        scales = [i for i in range(1, max(max_x, max_y) + 1)]
    else:
        scales = [2]

    for coords in antennae.values():
        for pt1, pt2 in combinations(coords, 2):
            diff1 = diff(pt1, pt2)
            diff2 = diff(pt2, pt1)
            for i in scales:
                for antinode in (add(pt1, scale(diff2, i)), add(pt2, scale(diff1, i))):
                    if (
                        antinode[0] >= 0
                        and antinode[0] <= max_x
                        and antinode[1] >= 0
                        and antinode[1] <= max_y
                    ):
                        antinodes.add(antinode)
    return len(antinodes)


def one(antennae, bounds):
    return solve(antennae, bounds, False)


def two(antennae, bounds):
    return solve(antennae, bounds, True)


def main():
    test_antennae, test_bounds = read_input("test.txt")
    assert one(test_antennae, test_bounds) == 14

    antennae, bounds = read_input("input.txt")
    print(one(antennae, bounds))

    print(two(test_antennae, test_bounds))
    print(two(antennae, bounds))


if __name__ == "__main__":
    main()
