import re


def read_input(filename):
    games = []
    with open(filename) as f:
        for stanza in f.read().split("\n\n"):
            lines = stanza.split("\n")
            game = {}
            for i, row_type in enumerate(("a", "b", "prize")):
                match = re.match(r"[^:]+: X([+=]\d+), Y([+=]\d+)", lines[i])
                x, y = int(match.group(1)[1:]), int(match.group(2)[1:])
                game[row_type] = (x, y)
            games.append(game)
    return games


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def solve(games, limit):
    score = 0
    for game in games:
        Tx, Ty = game["prize"]
        dxa, dya = game["a"]
        dxb, dyb = game["b"]

        D = det((dxa, dxb), (dya, dyb))

        n_a_num = det((Tx, dxb), (Ty, dyb))
        n_b_num = det((dxa, Tx), (dya, Ty))

        n_a = n_a_num // D
        n_b = n_b_num // D

        if (
            D != 0
            and n_a_num % D == 0
            and n_b_num % D == 0
            and (limit is None or (n_a < limit and n_b < limit))
        ):
            score += 3 * n_a + n_b
    return score


def one(games):
    return solve(games, 100)


def two(games):
    offset = 10000000000000
    games = [
        {"a": game["a"], "b": game["b"], "prize": game["prize"]} for game in games
    ]  # deep copy games for fun

    for game in games:
        game["prize"] = (game["prize"][0] + offset, game["prize"][1] + offset)

    return solve(games, None)


def main():
    test_games = read_input("test.txt")
    assert one(test_games) == 480

    games = read_input("input.txt")

    print(one(games))
    print(two(games))


if __name__ == "__main__":
    main()
