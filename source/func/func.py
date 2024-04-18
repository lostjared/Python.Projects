import sys

def func_nested(x):
    def test():
        return x*x
    
    return test

def func_call(x):
    return x()

def main(args):
    x = func_nested(10)
    print(x())
    print(func_call(x))

if __name__ == "__main__":
    sys.exit(main(sys.argv))