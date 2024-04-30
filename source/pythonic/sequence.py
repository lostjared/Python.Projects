import sys

class Vector:
    def __init__(self, seq):
        self.seq = seq;

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

def main(args):
    v2 = Vector([2, 4, 6, 8])
    for i in v2:
        print(i)
      
    print("Length: " + str(len(v2)))
    v1 = Vector((1,2))
    print(v1)
    print(repr(v1))



if __name__ == "__main__":
    sys.exit(main(sys.argv))
