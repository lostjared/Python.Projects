import sys
import scanner
import token


def scan(file):
    with open(file) as fp:
        scan = scanner.Scanner(fp.read())
        tokens = list()
        while scan.next():
            tokens.append(token.Token(scan.token.text, scan.token.type))
            scan.token.clear()
        return tokens

def main(args):
    if len(args) >= 2:
        tokens = scan(args[1])
        for i in tokens:
            i.print()
    else:
        print("requires one argument txt file")

if __name__ == "__main__":
    sys.exit(main(sys.argv))