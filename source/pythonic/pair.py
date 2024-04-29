import sys

# A Pythonic class implements these methods and moree

class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "Pair"
    def __str__(self):
        return "{%d, %d}" %(self.x, self.y)
    def __hash__(self):
        return hash(self.x, self.y)
    def __len__(self):
        return 2
    def __eq__(self, obj):
        if self.x == obj.x and self.y == obj.y:
            return True
        return False
    def __lt__(self, obj):
        if self.x < obj.x and self.y < obj.y:
            return True
        return False
   #imeplement more

def main(args):
    p = Pair(100, 100)
    t = { "one": p , "two": Pair(200, 200)}
    print(t["one"])
    p2 = Pair(101, 100)
    if p == p2:
        print("no way")
    else:
        print("yeah")
    print(repr(p))
    print(str(p2))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
