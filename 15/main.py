def read_input(filename):
    warehouse = {}
    with open(filename) as f:
        contents = f.read()
        raw_map, moves = contents.split("\n\n")
        for y, line in enumerate(raw_map.split("\n")):
            for x, c in enumerate(line):
                if c == "@":
                    robot = (x, y)
                else:
                    warehouse[(x, y)] = c

    moves = moves.replace("\n", "")
    return warehouse, moves, robot


def rescale_input(old_warehouse, robot):
    warehouse = {}
    robot = (2 * robot[0], robot[1])

    max_x = max(x for x, _ in old_warehouse.keys())
    max_y = max(y for _, y in old_warehouse.keys())

    for (x, y), c in old_warehouse.items():
        if c == "#":
            warehouse[(2 * x, y)] = "#"
            warehouse[(2 * x + 1, y)] = "#"
        if c == "O":
            warehouse[(2 * x, y)] = "["
            warehouse[(2 * x + 1, y)] = "]"

    for x in range(max_x):
        for y in range(max_y):
            if warehouse.get((2 * x, y)) is None:
                warehouse[(2 * x, y)] = "."

            if warehouse.get((2 * x + 1, y)) is None:
                warehouse[(2 * x + 1, y)] = "."
    return warehouse, robot


def print_warehouse(warehouse, robot):
    max_y = max(y for x, y in warehouse.keys())
    max_x = max(x for x, y in warehouse.keys())

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) == robot:
                print("@", end="")
            else:
                print(warehouse[(x, y)], end="")
        print()


def move_1(warehouse, direction, robot):
    directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

    max_x = max(x for x, _ in warehouse.keys())
    max_y = max(y for _, y in warehouse.keys())

    dx, dy = directions[direction]

    temp_x, temp_y = robot[0], robot[1]
    while True:
        temp_x += dx
        temp_y += dy
        if (
            temp_x < 0
            or temp_y < 0
            or temp_x > max_x
            or temp_y > max_y
            or warehouse[(temp_x, temp_y)] == "#"
        ):
            return robot
        elif warehouse[(temp_x, temp_y)] == ".":
            break

    while temp_x != robot[0] or temp_y != robot[1]:
        try:
            warehouse[(temp_x, temp_y)] = warehouse[(temp_x - dx, temp_y - dy)]
        except KeyError:
            pass
        temp_x -= dx
        temp_y -= dy

    warehouse[(robot[0], robot[1])] = "."
    warehouse[(robot[0] + dx, robot[1] + dy)] = "."

    robot = (robot[0] + dx, robot[1] + dy)
    return robot


def move_2(warehouse, direction, robot):
    directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

    max_x = max(x for x, y in warehouse.keys())
    max_y = max(y for x, y in warehouse.keys())

    dx, dy = directions[direction]

    temp_x, temp_y = robot[0], robot[1]
    while True:
        temp_x += dx
        temp_y += dy
        if (
            temp_x < 0
            or temp_y < 0
            or temp_x > max_x
            or temp_y > max_y
            or warehouse[(temp_x, temp_y)] == "#"
        ):
            return robot
        elif warehouse[(temp_x, temp_y)] == ".":
            break

    while temp_x != robot[0] or temp_y != robot[1]:
        try:
            warehouse[(temp_x, temp_y)] = warehouse[(temp_x - dx, temp_y - dy)]
        except KeyError:
            pass
        temp_x -= dx
        temp_y -= dy

    warehouse[(robot[0], robot[1])] = "."
    warehouse[(robot[0] + dx, robot[1] + dy)] = "."

    robot = (robot[0] + dx, robot[1] + dy)
    return robot


def score_1(warehouse):
    return sum(100 * y + x for (x, y), k in warehouse.items() if k == "O")


def score_2(warehouse):
    return sum(100 * y + x for (x, y), k in warehouse.items() if k == "[")


def one(warehouse, moves, robot):
    for m in moves:
        robot = move_1(warehouse, m, robot)
    return score_1(warehouse)


def can_move_vertically_2(pos, direction, warehouse):
    if warehouse[pos] == "[":
        d = 1
    elif warehouse[pos] == "]":
        d = -1
    else:
        return warehouse[pos] == "."  # can move if the space is empty

    # if both spaces are empty we can move
    if (
        warehouse[(pos[0], pos[1] + direction)] == "."
        and warehouse[(pos[0] + d, pos[1] + direction)] == "."
    ):
        return True

    # if either of the two spaces is a wall we can't move
    if (
        warehouse[(pos[0], pos[1] + direction)] == "#"
        or warehouse[(pos[0] + d, pos[1] + direction)] == "#"
    ):
        return False

    # we can also move if the two blocks above us can move (if one ore more of them is a block)
    return can_move_vertically_2(
        (pos[0] + d, pos[1] + direction), direction, warehouse
    ) and can_move_vertically_2((pos[0], pos[1] + direction), direction, warehouse)


def move_vertically_2(pos, direction, warehouse):
    if warehouse[pos] == "]":
        d = -1
    elif warehouse[pos] == "[":
        d = 1
    else:
        return

    while (
        warehouse[(pos[0], pos[1] + direction)] != "."
        or warehouse[(pos[0] + d, pos[1] + direction)] != "."
    ):
        move_vertically_2((pos[0], pos[1] + direction), direction, warehouse)
        move_vertically_2((pos[0] + d, pos[1] + direction), direction, warehouse)
    warehouse[(pos[0], pos[1] + direction)] = warehouse[pos]
    warehouse[(pos[0] + d, pos[1] + direction)] = warehouse[(pos[0] + d, pos[1])]
    warehouse[pos] = "."
    warehouse[(pos[0] + d, pos[1])] = "."


def can_move_horizontally_2(pos, direction, warehouse):
    if warehouse[(pos[0] + 2 * direction, pos[1])] == "#":
        return False
    if warehouse[(pos[0] + 2 * direction, pos[1])] == ".":
        return True

    return can_move_horizontally_2(
        (pos[0] + 2 * direction, pos[1]), direction, warehouse
    )


def move_horizontally_2(pos, direction, warehouse):
    while warehouse[(pos[0] + 2 * direction, pos[1])] != ".":
        move_horizontally_2((pos[0] + 2 * direction, pos[1]), direction, warehouse)
    warehouse[(pos[0] + 2 * direction, pos[1])] = warehouse[
        (pos[0] + direction, pos[1])
    ]
    warehouse[(pos[0] + direction, pos[1])] = warehouse[pos]
    warehouse[pos] = "."


def two(warehouse, moves, robot):
    directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    for m in moves:
        next_robot = (robot[0] + directions[m][0], robot[1] + directions[m][1])
        if warehouse[next_robot] == "#":
            continue
        elif warehouse[next_robot] == ".":
            robot = next_robot
        else:
            if m in "<>" and can_move_horizontally_2(
                next_robot, directions[m][0], warehouse
            ):
                move_horizontally_2(next_robot, directions[m][0], warehouse)
                robot = next_robot
            elif m in "^v" and can_move_vertically_2(
                next_robot, directions[m][1], warehouse
            ):
                move_vertically_2(next_robot, directions[m][1], warehouse)
                robot = next_robot
    return score_2(warehouse)


def main():
    warehouse, moves, robot = read_input("test1.txt")
    assert 2028 == one(warehouse, moves, robot)

    warehouse, moves, robot = read_input("test2.txt")
    assert 10092 == one(warehouse, moves, robot)

    warehouse, moves, robot = read_input("input.txt")
    print(one(warehouse, moves, robot))

    warehouse, moves, robot = read_input("test2.txt")
    warehouse, robot = rescale_input(warehouse, robot)
    assert two(warehouse, moves, robot) == 9021

    warehouse, moves, robot = read_input("input.txt")
    warehouse, robot = rescale_input(warehouse, robot)
    print(two(warehouse, moves, robot))


if __name__ == "__main__":
    main()
