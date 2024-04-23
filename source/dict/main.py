import sys

def main(args):
    d = { "apples": "fruit", "chicken":"meat", "computer":"electronics"}
    print(d)
    for i in sorted(d.keys()):
        print("%s:%s" %(i, d[i]))

    d["apples"] += "!"
    
    for i in d["apples"]:
        print("%c" % (i))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))