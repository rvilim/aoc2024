from collections import defaultdict


def read_input(filename):
    connections = defaultdict(set)
    with open(filename) as f:
        for line in f.readlines():
            c1, c2 = line.strip().split("-")
            connections[c1].add(c2)
            connections[c2].add(c1)

    return connections


def one(connections):
    groups = []
    for c1, c2s in connections.items():
        for c2 in c2s:
            if c1 > c2:
                continue
            for c3 in connections[c2]:
                if c2 > c3:
                    continue
                if c1 in connections[c3] and any(
                    c.startswith("t") for c in (c1, c2, c3)
                ):
                    groups.append((c1, c2, c3))

    return len(groups)


def find_clique(connections, seed_node):
    clique = set([seed_node])
    seen = set([seed_node])
    # start out with seed node add it to the clique
    # for each of the neighbours of each of the confirmed members, if it is connected to all the confirmed members, add it
    todo = connections[seed_node].copy()

    while todo:
        cur = todo.pop()

        # if all the members of the running clique are connected to the current node
        if all(cur in connections[confirmed] for confirmed in clique):
            # then this node should be a member of the clique too
            clique.add(cur)

            # then we add all the connections of the current node to our todo pile
            # (we are removing the ones that we've already looked at, e.g. "- seen")
            todo |= connections[cur] - seen

            # then add all the connections we just looked at to seen
            seen |= connections[cur]

    return clique


def two(connections):
    max_clique = set()
    for seed in connections.keys():
        c = find_clique(connections, seed)

        if len(c) > len(max_clique):
            max_clique = c

    return ",".join(sorted(max_clique))


def main():
    test_input = read_input("test.txt")
    assert 7 == one(test_input)

    real_input = read_input("input.txt")

    assert two(test_input) == "co,de,ka,ta"

    print(two(real_input))


if __name__ == "__main__":
    main()
