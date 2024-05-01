import sys
import abc

class Bird(abc.ABC):
    @abc.abstractmethod
    def quack(self):
        pass


class Duck(Bird):
    def __init__(self, name):
        self.name = name
    def quack(self):
        print("%s: quack" %(self.name))
    
class Goose(Bird):
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
