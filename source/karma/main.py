import sys

def give():
    print("enter thought: ")
    sys.stdout.flush()
    input = sys.stdin.readline()
    input = input[:-1]
    return input

def get(thought):
    if thought == "fear":
        return "0"
    elif  thought == "love":
        return "1"
    return thought

def main(args):
    print("birth")
    thoughts = []
    while True:
         thought = get(give())
         if thought == "death":
             break
         print("I thought: %s"%(thought))
         thoughts.append(thought)
         
    print("in this life you thought: ")
    for i in thoughts:
        print(i)
    print(thought)
    return main(args)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
