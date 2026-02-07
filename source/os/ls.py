
import os, sys

def printDir(d):
	ls = os.listdir(d)
	index = 0
	for i in ls:
		print("File (%d): %s\n" %(index, i))
		index += 1
	return 0

if __name__ == "__main__":
	input = input()
	printDir(input)


