import copy

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def print_grid(grid):
    for row in grid:
        print("".join(row))


def rotate_right(dir):
    if dir == UP:
        return RIGHT
    elif dir == RIGHT:
        return DOWN
    elif dir == DOWN:
        return LEFT
    elif dir == LEFT:
        return UP


def input(filename):
    with open(filename) as f:
        grid = [list(line.strip()) for line in f]

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "^":
                return (i, j), UP, grid


def step(pos, dir, grid):
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])

    if (
        new_pos[0] < 0
        or new_pos[0] >= len(grid)
        or new_pos[1] < 0
        or new_pos[1] >= len(grid[0])
    ):
        raise Exception("Out of bounds")
    if grid[new_pos[0]][new_pos[1]] == "#":
        return pos, rotate_right(dir), grid
    grid[new_pos[0]][new_pos[1]] = "X"
    return new_pos, dir, grid


def simulate(pos, dir, grid):
    pos = tuple(pos)
    dir = tuple(dir)

    visited = set((pos, dir))
    while True:
        try:
            pos, dir, grid = step(pos, dir, grid)
            if (pos, dir) in visited:
                return grid, True
            visited.add((pos, dir))
        except:
            break
    return grid, False


def one(pos, dir, grid):
    grid[pos[0]][pos[1]] = "X"
    grid, _ = simulate(pos, dir, grid)
    visited = []
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "X":
                visited.append((i, j))

    return sum([row.count("X") for row in grid]), visited


def two(pos, dir, grid, visited):
    n_loops = 0

    for obs in visited:
        obs_row, obs_col = obs

        if (obs_row == pos[0] and obs_col == pos[1]) or grid[obs_row][obs_col] == "#":
            continue

        new_grid = copy.deepcopy(grid)
        new_grid[obs_row][obs_col] = "#"
        g, in_loop = simulate(pos, dir, new_grid)

        n_loops += in_loop
    return n_loops


def main():
    test_pos, test_dir, test_grid = input("test.txt")
    assert 41 == one(test_pos, test_dir, test_grid)[0]

    pos, dir, grid = input("input.txt")
    n, visited = one(pos, dir, grid)
    print(n)

    _, test_visited = one(test_pos, test_dir, test_grid)
    assert 6 == two(test_pos, test_dir, test_grid, test_visited)
    print(two(pos, dir, grid, visited))


if __name__ == "__main__":
    main()
