from collections import defaultdict
from functools import cache


def read_input(filename):
    with open(filename) as f:
        return list(map(int, f.read().split("\n")))


def step(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


def one(secrets):
    res = 0
    for secret in secrets:
        for _ in range(2000):
            secret = step(secret)
        res += secret

    return res


def two(secrets):
    profits = defaultdict(int)
    for secret in secrets:
        pattern = (None, None, None, None)
        prev_price = secret % 10

        seen_patterns = set()
        for _ in range(2000):
            secret = step(secret)

            price = secret % 10
            pattern = pattern[1:] + (price - prev_price,)

            if pattern not in seen_patterns:
                profits[pattern] += price
                seen_patterns.add(pattern)
            prev_price = price

    # max_profit = max(profits.values())
    max_profit = max(v for k, v in profits.items() if None not in k)
    return max_profit


def main():
    secrets_test_1 = read_input("test1.txt")

    assert one(secrets_test_1) == 37327623

    secrets = read_input("input.txt")
    print(one(secrets))

    secrets_test_2 = read_input("test2.txt")
    assert two(secrets_test_2) == 23
    print(two(secrets))


if __name__ == "__main__":
    main()
