import sys

def print_data(data):
    for i in data:
        print("%c"%(i), end="")

def read_data(filename):
     f = open(filename)
     return f.read()

def proc_file(data):
     if len(data) == 0:
         print("Could not read from file: %s"%(filename))
         return
     
     print("data = [", end="")
     for i in range(0, len(data)-1):
        print("0x{:02X}, ".format(ord(data[i])), end="")
     print("0x{:02X}]".format(ord(data[len(data)-1])))
  
def main(args):
    if len(args) >= 2:
        for i in range(1, len(args)):
            proc_file(read_data(args[i]))
    else:
        proc_file(sys.stdin.read())
    
    return  0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
