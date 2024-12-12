def read_input(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().strip().split(" ")]

def blink(num):
    if num==0:
        return [1]
    elif len(str(num))%2==0:
        s=str(num)
        return [int(s[:len(s)//2]), int(s[len(s)//2:])]
    return [num*2024]

def n_stones(num, n_blinks, cache):
    if n_blinks==0:
        return 1
    if (num, n_blinks) in cache:
        return cache[(num, n_blinks)]
    
    count=0
    for n in blink(num):
        count+=n_stones(n, n_blinks-1, cache)

    cache[(num, n_blinks)]=count
    return count

def one_two(input_stones, n_blinks):
    cache = {}
    return sum(n_stones(num, n_blinks, cache) for num in input_stones)

def main():
    test_input = read_input('test.txt')
    
    assert 22==one_two(test_input, 6)
    assert 55312==one_two(test_input, 25)

    input = read_input('input.txt')

    print(one_two(input, 25))
    print(one_two(input, 75))
if __name__=="__main__":
    main()