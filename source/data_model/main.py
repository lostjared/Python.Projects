import sys


class Three:
    def __init__(self):
        self.t = [1,2,3]
    def __len__(self):
        return len(self.t)
    def __getitem__(self, item):
        return self.t[item]
    def __str__(self):
        return "As String: " + str(self.t)

class Test(Three):
    def __init__(self):
        Three()
    def print_hello(self, s):
            print("Hello: d" + str(s))    

def main(args):
    print("Hello, World!")
    t = Three()
    print("Three %d" % (len(t)))
    print("Index zero: %d " %(t[0]))

    for i in sorted(t):
        print("Index: %d"%(i))
    for i in reversed(t):
        print("Reversed: %d" %(i))

    print(t)
    t2 = Test()
    t2.print_hello("Hello ")

if __name__ == "__main__":
    sys.exit(main(sys.argv))

