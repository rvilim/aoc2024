def print_grid(grid):
    max_x = max([x for x, y in grid])
    max_y = max([y for _, y in grid])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid[complex(x, y)], end="")
        print("")


def score_one(grid, point):
    if grid[point] == 9:
        return {(point)}
    else:
        peaks = set()
        for next_diff in [complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)]:
            if point + next_diff in grid and grid[point + next_diff] == grid[point] + 1:
                peaks = peaks.union(score_one(grid, point + next_diff))

        return peaks


def score_two(grid, point):
    if grid[point] == 9:
        return 1
    else:
        s = 0
        for next_diff in [complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)]:
            if point + next_diff in grid and grid[point + next_diff] == grid[point] + 1:
                s += score_two(grid, point + next_diff)

        return s


def read_input(filename):
    topo_map = {}
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                topo_map[complex(x, y)] = int(char)

    trailheads = tuple([k for k, v in topo_map.items() if v == 0])
    return topo_map, trailheads


def one(topo_map, trailheads):
    return sum(len(score_one(topo_map, trailhead)) for trailhead in trailheads)


def two(topo_map, trailheads):
    return sum(score_two(topo_map, trailhead) for trailhead in trailheads)


def main():
    test_topo_map, test_trailheads = read_input("test.txt")

    assert 36 == one(test_topo_map, test_trailheads)

    topo_map, trailheads = read_input("input.txt")
    print(one(topo_map, trailheads))

    print(two(test_topo_map, test_trailheads))
    print(two(topo_map, trailheads))


if __name__ == "__main__":
    main()
