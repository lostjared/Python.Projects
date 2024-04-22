import sys
import scanner
import token

def main(args):
    if len(args) >= 2:
        scan = scanner.Scanner(open(args[1]).read())
        print (scan.input)
        while scan.next():
            token = scan.token
            print(token.text + ": " + token.type)
            token.clear()



if __name__ == "__main__":
    sys.exit(main(sys.argv))