def read_input(filename):
    a = []
    for line in open(filename).readlines():
        a.append([int(char.strip()) for char in line.split(" ")])
    return a


def check_sample(levels):
    sorted_condition = (
        sorted(levels) == levels or sorted(levels, reverse=True) == levels
    )
    diff_condition = all(
        1 <= abs(levels[i] - levels[i + 1]) <= 3 for i in range(len(levels) - 1)
    )
    return sorted_condition and diff_condition


def one(input):
    return sum(check_sample(levels) for levels in input)


def two(input):
    n_good = 0
    for levels in input:
        if check_sample(levels):
            n_good += 1
        else:
            if any(
                check_sample(levels[:i] + levels[i + 1 :]) for i in range(len(levels))
            ):
                n_good += 1

    return n_good


def main():
    test_input = read_input("test.txt")
    # print([check_sample_one(levels) for levels in test_input])
    assert one(test_input) == 2

    input = read_input("input.txt")
    print(one(input))

    print(two(test_input))
    assert two(test_input) == 4

    input = read_input("input.txt")
    print(two(input))


if __name__ == "__main__":
    main()
