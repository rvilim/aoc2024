from functools import cache


def read_input(file):
    with open(file) as f:
        towels, patterns = f.read().split("\n\n")

        towels = tuple(towels.split(", "))
        patterns = tuple(patterns.split("\n"))

    return towels, patterns


def solve_one(towels, pattern):
    for towel in towels:
        if (
            pattern == towel
            or pattern.startswith(towel)
            and solve_one(towels, pattern[len(towel) :])
        ):
            return True

    return False


@cache
def solve_two(towels, pattern):
    n_combos = 0
    if not pattern:
        return 1

    for towel in towels:
        if len(pattern) >= len(towel) and all(p == t for p, t in zip(pattern, towel)):
            n_combos += solve_two(towels, tuple(pattern[len(towel) :]))
    return n_combos


def one(towels, patterns):
    return sum(solve_one(towels, pattern) for pattern in patterns)


def two(towels, patterns):
    s = 0
    for pattern in patterns:
        s += solve_two(towels, pattern)
    return s


def main():
    towels, patterns = read_input("test.txt")

    assert 6 == one(towels, patterns)

    towels, patterns = read_input("input.txt")
    print(one(towels, patterns))

    towels, patterns = read_input("test.txt")
    assert 16 == two(towels, patterns)

    towels, patterns = read_input("input.txt")
    print(two(towels, patterns))


if __name__ == "__main__":
    main()
