import sys

class Obj:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "Obj"
    
class Person(Obj):
    def __init__(self, name, first):
        super().__init__(name)
        self.first = first
    def __str__(self):
        return super().__str__() + " " + self.first
    def __repr__(self):
        return "Person"

def main(args):
    p = Person("Human", "Jared")
    print(p)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
