import sys

def func_nested(x):
    def test():
        return x*x
    return test

def main(args):
    x = func_nested(10)
    print(x())



sys.exit(main(sys.argv))
