
import os, sys

def printDir(d):
	ls = os.listdir(d)
	for i in ls:
		print("File: %s\n" %(i))
	return 0



if __name__ == "__main__":
	printDir(".")


