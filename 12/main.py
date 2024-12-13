def read_input(filename):
    garden = {}
    for y, line in enumerate(open(filename)):
        for x, plot in enumerate(line.strip()):
            garden[(x, y)] = plot

    return garden


def get_side(region, point, face):
    move_deltas = {
        (-1, 0): ((0, 1), (0, -1)),
        (1, 0): ((0, 1), (0, -1)),
        (0, 1): ((1, 0), (-1, 0)),
        (0, -1): ((1, 0), (-1, 0)),
    }

    side = set((point,))

    face_x, face_y = face
    for move_delta in move_deltas[face]:
        x, y = point
        dx, dy = move_delta
        while True:
            x += dx
            y += dy
            if (x, y) not in region or (x + face_x, y + face_y) in region:
                break
            side.add((x, y))
    return tuple(sorted(side))


def get_sides(region):
    seen_sides = set()

    for point in region:
        for face in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            dx, dy = face
            if (point[0] + dx, point[1] + dy) not in region:
                seen_sides.add((face, get_side(region, point, face)))
    return seen_sides


def get_perimeter_1(region):
    perimeter = 0
    for point in region:
        x, y = point
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if (x + dx, y + dy) not in region:
                perimeter += 1
    return perimeter


def get_perimeter_2(region):
    return len(get_sides(region))


def get_regions(garden):
    visited = set()
    regions = []
    for (x, y), plot in garden.items():
        if (x, y) in visited:
            continue
        s = [(x, y)]
        curr_plot_type = garden[(x, y)]
        cur_region = set()
        while s:
            x, y = s.pop()
            if (x, y) in cur_region or (x, y) in visited:
                continue
            cur_region.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                if (x + dx, y + dy) in garden and garden[
                    (x + dx, y + dy)
                ] == curr_plot_type:
                    s.append((x + dx, y + dy))
        visited.update(cur_region)
        regions.append((curr_plot_type, cur_region))
    return regions


def one(garden):
    regions = get_regions(garden)
    return sum(get_perimeter_1(points) * len(points) for _, points in regions)


def two(garden):
    regions = get_regions(garden)
    return sum(get_perimeter_2(points) * len(points) for _, points in regions)


def main():
    test_garden_1 = read_input("test1.txt")
    assert 140 == one(test_garden_1)

    test_garden_2 = read_input("test2.txt")
    assert 772 == one(test_garden_2)

    test_garden_3 = read_input("test3.txt")
    assert 1930 == one(test_garden_3)

    input_garden = read_input("input.txt")
    print(one(input_garden))

    assert 80 == two(test_garden_1)
    assert 436 == two(test_garden_2)
    assert 1206 == two(test_garden_3)

    test_garden_4 = read_input("test4.txt")
    assert 236 == two(test_garden_4)

    test_garden_5 = read_input("test5.txt")
    assert 368 == two(test_garden_5)

    print(two(input_garden))


if __name__ == "__main__":
    main()
