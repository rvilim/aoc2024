from functools import cache

# these are in row,col order
numpad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
numpad_rev = {v: k for k, v in numpad.items()}

dirpad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}
dirpad_rev = {v: k for k, v in dirpad.items()}


def get_paths(start, end, pad):
    def _get_paths_e2s(start, end, pad):
        if start not in pad.values():
            return []

        if start == end:
            return ["A"]

        ret = []
        if start[0] < end[0]:
            for r in _get_paths_e2s((start[0] + 1, start[1]), end, pad):
                ret.append(r + "v")
        if start[0] > end[0]:
            for r in _get_paths_e2s((start[0] - 1, start[1]), end, pad):
                ret.append(r + "^")

        if start[1] < end[1]:
            for r in _get_paths_e2s((start[0], start[1] + 1), end, pad):
                ret.append(r + ">")

        if start[1] > end[1]:
            for r in _get_paths_e2s((start[0], start[1] - 1), end, pad):
                ret.append(r + "<")

        return ret

    # This is dumb but my recursive function generates paths backward,
    # this just reverses them
    for rev_path in _get_paths_e2s(start, end, pad):
        yield rev_path[::-1]


@cache
def move(start, end, layer, num_layers):
    shortest = float("inf")
    if layer == num_layers - 1:  # if we are on the last layer we just directly press it
        return 1

    if layer == 0:
        paths_gen = get_paths(numpad[start], numpad[end], numpad)
    else:
        paths_gen = get_paths(dirpad[start], dirpad[end], dirpad)

    cur = "A"

    for path in paths_gen:
        length = 0
        for goal in path:
            length += move(cur, goal, layer + 1, num_layers)
            cur = goal
        shortest = min(shortest, length)
    return shortest


def read_input(filename):
    with open(filename) as f:
        return f.read().split("\n")


def solve(code, n_pads):
    cur = "A"
    m = 0
    n = int(code[:-1])
    for target in code:
        m += move(cur, target, 0, n_pads)
        cur = target

    return m * n


def one(codes):
    return sum(solve(code, 4) for code in codes)


def two(codes):
    return sum(solve(code, 27) for code in codes)


def main():
    test = read_input("test.txt")
    assert one(test) == 126384

    input_codes = read_input("input.txt")
    print(one(input_codes))
    print(two(input_codes))


if __name__ == "__main__":
    main()
