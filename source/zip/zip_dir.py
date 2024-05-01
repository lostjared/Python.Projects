import sys
import zipfile
import os

def zip_directory(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, os.path.join(folder_path, '..')))

def main(args):
    if len(args) >= 2:
        zip_directory(args[1], args[2])
        print("%s -> %s" %(args[1], args[2]))
    return 0
\
if __name__ == "__main__":
    sys.exit(main(sys.argv))
