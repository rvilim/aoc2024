def read_input(filename):
    list_grid = []
    grid = {}

    with open(filename) as file:
        for line in file:
            list_grid.append(list(line.strip()))

    for y in range(len(list_grid)):
        grid[y] = {}
        for x in range(len(list_grid[y])):
            grid[y][x] = list_grid[y][x]

    return grid


def check_line_xmas(grid, x, y, delta):
    try:
        if (
            grid[y][x] == "X"
            and grid[y + delta[0]][x + delta[1]] == "M"
            and grid[y + delta[0] * 2][x + delta[1] * 2] == "A"
            and grid[y + delta[0] * 3][x + delta[1] * 3] == "S"
        ):
            return True
    except KeyError:
        pass
    return False


def check_line_x_mas(grid, x, y, delta):
    template_1 = ["M", "A", "S"][:: delta[0]]
    template_2 = ["M", "A", "S"][:: delta[1]]
    try:
        if (
            grid[y][x] == template_1[0]
            and grid[y + 1][x + 1] == template_1[1]
            and grid[y + 2][x + 2] == template_1[2]
            and grid[y][x + 2] == template_2[0]
            and grid[y + 1][x + 1] == template_2[1]
            and grid[y + 2][x] == template_2[2]
        ):
            return True
    except KeyError:
        pass

    return False


def check_position_one(grid, x, y):
    n = 0
    for delta in [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]:
        n += check_line_xmas(grid, x, y, delta)

    return n


def check_position_two(grid, x, y):
    n = 0
    for delta in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
        n += check_line_x_mas(grid, x, y, delta)

    return n


def one(grid):
    s = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            s += check_position_one(grid, x, y)
    return s


def two(grid):
    s = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            s += check_position_two(grid, x, y)
    return s


def main():
    test_grid = read_input("test.txt")
    assert one(test_grid) == 18

    input_grid = read_input("input.txt")
    print(one(input_grid))

    assert two(test_grid) == 9
    print(two(input_grid))


if __name__ == "__main__":
    main()
