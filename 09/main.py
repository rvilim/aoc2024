def read_input(filename):
    disk = {}
    with open(filename) as f:
        line = f.readline().strip()
        # for i, char in enumerate(line):
            # print(i, char)
        id=0
        pos=0
        for i, char in enumerate(line):
            if i%2==0:
                for j in range(int(char)):
                    disk[pos] = id
                    pos+=1
                id+=1
            else:
                for j in range(int(char)):
                    disk[pos] = '.'
                    pos+=1

    return disk 

def print_disk(disk):
    for i in range(len(disk)):
        print(disk[i], end="")
    print("")

def checksum(disk):
    s = 0
    for i in range(len(disk)):
        if disk[i] != '.':
            s+=i*disk[i]
    return s

def one(disk):
    first_idx = 0
    last_idx = len(disk)-1

    while disk[first_idx] != '.':
        first_idx+=1
    while disk[last_idx] == '.':
        last_idx-=1

    while first_idx < last_idx:
        if disk[last_idx] == '.':
            last_idx-=1
        elif disk[first_idx] != '.':
            first_idx+=1
        else:
            disk[first_idx] = disk[last_idx]
            disk[last_idx] = '.'
            first_idx+=1
            last_idx-=1

    return checksum(disk)

def find_file_start(disk, idx):
    assert disk[idx] != '.','no file at that location'
    id = disk[idx]
    end_idx = idx
    while idx!=0 and disk[idx] == id:
        idx-=1
    return idx+1, end_idx-idx

def find_free_blocks(disk, min_length):
    i = 0
    while i < len(disk):
        if disk[i] == '.':
            start = i
            while i < len(disk) and disk[i] == '.':
                i += 1
            if i-start >= min_length:
                return start
        else:
            i += 1
    return None

def two(disk):
    last_idx = len(disk)-1

    while disk[last_idx] == '.':
        last_idx-=1

    while last_idx > 0:
        if disk[last_idx] == '.':
            last_idx-=1
        else:
            file_start, file_length = find_file_start(disk, last_idx)
            block_start = find_free_blocks(disk, file_length)
            if block_start is not None and block_start < file_start:
                for i in range(file_length):
                    disk[block_start+i] = disk[file_start+i]
                for i in range(file_length):
                    disk[file_start+i] = '.'
                
            last_idx = file_start-1
        
    return checksum(disk)
def main():
    assert one(read_input('test.txt'))==1928

    print(one(read_input('input.txt')))

    assert 2858==two(read_input('test.txt'))

    print(two(read_input('input.txt')))
if __name__=="__main__":
    main()
