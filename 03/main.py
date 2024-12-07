import re

def read_input(filename):
    with open(filename) as file:
        return file.read()
    
def extract_mul(input):
    return re.findall(r'mul\(\d{,3},\d{,3}\)',input)

def remove_dont(input):
    input = input.replace('\n', '')
    return re.sub(r"don't\(\)(.*?do\(\)|.*)", "", input)

def two(input):
    input = remove_dont(input)
    extracted = extract_mul(input)
    s = 0
    for m in extracted:
        a,b = m.split(',')
        s+=int(a[4:])*int(b[:-1])
    return s

def one(input):
    extracted = extract_mul(input)
    s = 0
    for m in extracted:
        a,b = m.split(',')
        s+=int(a[4:])*int(b[:-1])
    return s

def main():
    test1 = read_input('test1.txt')
    assert one(test1)==161

    input = read_input('input.txt')
    print(one(input))

    test2 = read_input('test2.txt')
    assert two(test2)==48

    input = read_input('input.txt')
    print(two(input))
if __name__=="__main__":
    main()