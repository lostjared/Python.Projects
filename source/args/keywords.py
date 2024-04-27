import sys

def test_out(**kw):
    if 'test' in kw:
        print(kw['test'])
    else:
        print("no test")


def main(args):
    test_out()
    test_out(test="Hello, World!")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    