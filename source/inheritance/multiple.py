import sys

class Obj:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "Obj"
    
class Hat:
    def __init__(self, type):
        self.type = type
    def wear(self):
        print("Wearing the %s" %(self.type))
    def h_type(self):
        return self.type
    
class Person(Obj, Hat):
    def __init__(self, name, first):
        Obj.__init__(self, name)
        Hat.__init__(self, "Fedora")
        self.first = first
    def __str__(self):
        return Obj.__str__(self) + " " + self.first + " wearing " +  Hat.h_type(self)
    def __repr__(self):
        return "Person"

def main(args):
    p = Person("Human", "Jared")
    print(p)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))