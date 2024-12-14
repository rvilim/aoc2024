from dataclasses import dataclass
from typing import Any
from math import gcd, lcm, log
from collections import Counter
from functools import cache, reduce
import cProfile, pstats


@dataclass()
class robot:
    x: int
    y: int
    vx: int
    vy: int

    def __repr__(self) -> str | tuple[Any, ...]:
        return f"({self.x},{self.y})#({self.vx},{self.vy})"


def read_input(filename):
    robots = []
    with open(filename) as f:
        for line in f:
            parts = line.strip().replace("p=", "").replace(" v=", ",").split(",")
            x, y, vx, vy = map(int, parts)
            robots.append(robot(x, y, vx, vy))
    return robots


def move(robots, size_x, size_y, t=1):
    if t == 1:
        for r in robots:
            r.x = (r.x + r.vx) % size_x
            r.y = (r.y + r.vy) % size_y
    else:
        for r in robots:
            r.x = (r.x + t * r.vx) % size_x
            r.y = (r.y + t * r.vy) % size_y
    return robots


def print_grid(robots, size_x, size_y):
    c = Counter((r.x, r.y) for r in robots)

    for y in range(size_y):
        for x in range(size_x):
            if c[(x, y)] != 0:
                print(c[(x, y)], end="")
            else:
                print(".", end="")
        print()


def score(robots, size_x, size_y):
    middle_x = size_x // 2
    middle_y = size_y // 2

    c = Counter(
        (round(r.x / size_x), round(r.y / size_y))
        for r in robots
        if r.x != middle_x and r.y != middle_y
    )
    return reduce(lambda x, y: x * y, c.values())


def one(robots, size_x, size_y):
    return score(move(robots, size_x, size_y, 100), size_x, size_y)


@cache
def cacheprob(c, l):
    return -(c / l) * log(c / l)


def get_entropy_dir(vals):
    ent = 0
    l = len(vals)
    for c in Counter(vals).values():
        ent += cacheprob(c, l)
    return ent


def get_entropy_mag(robots):
    x = [r.x for r in robots]
    y = [r.y for r in robots]
    return get_entropy_dir(x) ** 2 + get_entropy_dir(y) ** 2


def robots_copy(robots):
    return [robot(r.x, r.y, r.vx, r.vy) for r in robots]


def two(robots, size_x, size_y):
    min_entropy = get_entropy_mag(robots)
    min_step = (0, robots_copy(robots))
    period = get_period(size_x, size_y, robots[0].vx, robots[0].vy)

    for i in range(period):
        move(robots, size_x, size_y, 1)

        if get_entropy_mag(robots) < min_entropy:
            min_entropy = get_entropy_mag(robots)
            min_step = (i + 1, robots_copy(robots))

    return min_step


def get_period(size_x, size_y, vx, vy):
    x_period = size_x // gcd(size_x, abs(vx))
    y_period = size_y // gcd(size_y, abs(vy))

    return lcm(x_period, y_period)


def main():
    test_size_x, test_size_y = 11, 7
    test_robots = read_input("test.txt")
    assert one(robots_copy(test_robots), test_size_x, test_size_y) == 12

    size_x, size_y = 101, 103
    robots = read_input("input.txt")
    print(one(robots_copy(robots), size_x, size_y))

    min_step, min_step_grid = two(robots_copy(robots), size_x, size_y)
    print(min_step)
    print_grid(min_step_grid, size_x, size_y)


if __name__ == "__main__":
    main()
