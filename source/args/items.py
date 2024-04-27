import sys

def writeln(*args):
    for i in args:
        print(i, end="")
    print("", end="\n")

def main(args):
    writeln("Hello, ", "World", "! ", 255)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    