import sys
import os

class Obj:
    def __init__(self):
        self.type = "Obj"
    def __str__(self):
        return self.type
    def __repr__(self):
        return self.type

class File(Obj):
    def __init__(self, path, dir):
        self.path = path
        self.dir = dir
    def __str__(self):
        if self.dir == True:
            return self.path + "/"
        return self.path
    def __repr__(self):
        return self.__str__()
class FileSystem(Obj):
    def __init__(self, path):
        lst = os.listdir(path)
        self.files = []
        for i in lst:
            self.files.append(File(i, False))
    def __str__(self):
        return str(self.files)
    def __len__(self):
        return len(self.files)
    def __getitem__(self, index):
        return self.files[index]

def main(args):
    if len(args) >= 2:
        fs = FileSystem(args[1])
        print(str(fs))
    else:
        print("argument: path")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))