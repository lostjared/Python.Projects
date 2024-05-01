import sys

class Duck:
    def __init__(self, name):
        self.name = name
    def quack(self):
        print("%s: quack" %(self.name))
    
class Goose:
    def __init__(self, name):
        self.name = name
    def quack(self):
        print("Goose: %s quack" % (self.name))


def say_hello(obj):
    obj.quack()

def main(args):
    duck = Duck("Bob")
    goose = Goose("Steve")
    say_hello(duck)
    say_hello(goose)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
