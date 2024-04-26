
import sys
import os

funcs = []

def register_call(start):
    def wrap():
        funcs.append(start.__name__)
        start()     
    return wrap

@register_call
def number1():
    print ("Number 1")
@register_call
def number2():
    print("Number 2")
def number3():
    print("number3")

def main():
    number1()
    number2()
    number3()
    for i in funcs:
        print("function name: %s" %(i))
    
if __name__ == "__main__":
    main()