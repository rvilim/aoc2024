import cProfile
import pstats
from functools import cache
def read_input(filename):
    eqs = []
    with open(filename) as f:
        for line in f:
            l = line.strip().split(': ')
            answer = l[0]
            operands = l[1].split(' ')
            eqs.append((int(answer), tuple(int(i) for i in operands)))
    return eqs

bconcat_cache = [-1] * 1000

def two_ops(a,b):
    return a*b, a+b, a * bconcat_cache[b] + b

def one_ops(a,b):
    return a+b, a*b

def solve(goal, eq, ops_fn):
    n_terms = len(eq)
    def solve_helper(i, running):
        if running>goal:
            return False
        
        if i==n_terms:
            return goal if running==goal else 0
        
        for op_res in ops_fn(running, eq[i]):
            if result := solve_helper(i+1, op_res):
                return result
            
        return False
    return solve_helper(1, eq[0])

def one(eqs):
    invalid_eqs=[]
    s = 0
    for i, eq in enumerate(eqs):
        res = solve(eq[0], eq[1], one_ops)
        if res:
            s += res
        else:
            invalid_eqs.append(i)
    return s, invalid_eqs

def two(eqs, prev_answer, prev_invalid_eqs):
    s = 0
    for eq_idx in prev_invalid_eqs:
        res = solve(eqs[eq_idx][0], eqs[eq_idx][1], two_ops)
        if res:
            s += res

    return s+prev_answer

def main(profile):
    global bconcat_cache

    if profile:
        profiler = cProfile.Profile()
        profiler.enable()
    
    test_eqs = read_input('test.txt')
    test_one_answer, test_one_invalid_eqs = one(test_eqs)

    assert 3749 == test_one_answer

    input = read_input('input.txt')

    for eq in input:
        for b in eq[1]:
            if bconcat_cache[b] == -1:
                bconcat_cache[b] = (10 ** len(str(b)))

    one_answer, one_invalid_eqs = one(input)
    print(one_answer)

    assert 11387 == two(test_eqs, test_one_answer, test_one_invalid_eqs)
    print(two(input, one_answer, one_invalid_eqs))

    if profile:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumulative')
        stats.print_stats()

if __name__=="__main__":
    main(False)
