import sys

def main(args):
    s = "Hello, World!"
    s1 = s[0:5]
    print(s1)
    s2 = s[7:]
    print(s2)
    f = s.find(", ")
    world = s[f+len(", "):]
    print(world)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
