import sys

class Vector:
    def __init__(self, seq):
        self.seq = seq
    def __len__(self):
        return len(self.seq)
    def __getitem__(self, index):
        return self.seq[index]
    def __iter__(self):
        return iter(self.seq)
    def __str__(self):
        return str(self.seq)
    def __repr__(self):
        return "Vector"
    def sum(self):
        total = 0
        for i in self.seq:
            total += i
        return total
    

def main(args):
    v2 = Vector([2, 4, 6, 8])
    for i in v2:
        print(i)
    total = v2.sum()
    print("sum is: %d"%(total))
    print("Length: " + str(len(v2)))
    v1 = Vector((1,2))
    print(v1)
    print(repr(v1))
    print(v1[0])

    v3 = Vector( [range(25) ])
    for i in v3:
        print(repr(i) + ": " + str(i))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
