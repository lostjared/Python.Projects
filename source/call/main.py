import sys

class Functor:
    def __init__(self, x):
        self.x = x
    def __call__(self): # call is like operator()
        return self.x * self.x

def main(args):
    x = Functor(100)
    print("x value: %d", x())


if __name__ == "__main__":
    sys.exit(main(sys.argv))