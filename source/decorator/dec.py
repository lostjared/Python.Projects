import sys

def exit_with_message(code):
    def goodbye(ec):
        print("Bye")
        code(ec)
    return goodbye

@exit_with_message
def Quit(ec):
    print("Exiting: %d" %(ec))
    sys.exit(ec)


Quit(0)




































