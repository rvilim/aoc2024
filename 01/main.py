from collections import Counter

def input(filename):
    l=[]
    r=[]

    for line in open(filename).readlines():
        l.append(int(line.split(' ')[0]))
        r.append(int(line.split(' ')[-1].strip()))

    return l,r

def dist1(l,r):
    return sum(
            abs(ri-li) for li,ri in zip(sorted(l),sorted(r))
        )

def dist2(l,r):
    rcounts = Counter(r)
    
    return sum(
        li*rcounts[li] for li in l
    )

def main():
    l,r = input('test.txt')
    assert 11==dist1(l,r)
    
    l,r = input('input.txt')
    print(dist1(l,r))


    l,r = input('test.txt')
    assert 31 == dist2(l,r)
    
    l,r = input('input.txt')
    print(dist2(l,r))

if __name__=="__main__":
    main()