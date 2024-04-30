import sys


class Stack:
    def __init__(self):
        self.stack = []
        self.index = 0
    def push(self, item):
        self.stack.append(item)
        self.index += 1
    def top(self):
        return self.stack[self.index-1]
    def bottom(self):
        return self.stack[0]
    def pop(self):
        self.index -= 1
        if self.index < 0:
            raise Exception
        last = self.stack[self.index]
        self.stack.pop()
        return last
    def __getitem__(self, index):
        return self.stack[index]
    def __len__(self):
        return len(self.stack)
    def __str__(self):
        return str(self.stack)
    def __repr__(self):
        return "Stack :[ %s ] " % (str(self.stack))
    def __hash__(self):
        return hash(self.stack)
    def __bytes__(self):
        return bytes(self.stack)

def main(args):
    stack = Stack()
    stack.push(41)
    stack.push(25)
    stack.push(32)
    last = stack.pop()
    print("last %d" % (last))
    for i in stack:
        print(i)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

