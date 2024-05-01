import sys
import re


def main(args): 
    expr = re.compile(r'\d')
    print("enter string to test")
    line = sys.stdin.readline()
    if expr.match(line):
        print("match")
    else:
        print("no match")
    matches = expr.split(line)
    print (matches)


    return 0



if __name__ == "__main__":
    sys.exit(main(sys.argv))
