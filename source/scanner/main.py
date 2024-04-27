import sys
import scanner
import scan_token


def scan(file):
    with open(file) as fp:
        scan = scanner.Scanner(fp.read())
        tokens = list()
        try: 
            while scan.next():
                tokens.append(scan_token.Token(scan.token.text, scan.token.type))
                scan.token.clear()
        except Exception:
            print ("Scanner: Syntax Error")
            sys.exit(1)

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