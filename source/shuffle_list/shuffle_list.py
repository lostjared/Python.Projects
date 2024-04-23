import sys
import random

def main(args):
    data = sys.stdin.read()
    lst = data.split("\n")
    random.shuffle(lst)
    for i in lst:
        print(i)  

if __name__ == "__main__":
    sys.exit(main(sys.argv))