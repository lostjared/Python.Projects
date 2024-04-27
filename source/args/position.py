import sys

def test_out(apples, **kw):
    print(apples + ": ", end="")
    if 'test' in kw:
        print(kw['test'])
    else:
        print("no test")

def hello(format, **kw):
    print(format + " ", end="")
    if 'world' in kw:
        print(kw['world'])

def hello_list(*w, **kw):
    for i in w:
        print(i, end="")
    print(": ", end="")
    for key in kw:
        print("key %s" %(key))
        print("value: %s" %(kw[key]))


def main(args):
    test_out("here")
    test_out("here is: ", test="Hello, World!")
    hello("test")
    hello("Hello, ", world="World!")
    hello_list(1,2,3, "Hello", word="words")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    