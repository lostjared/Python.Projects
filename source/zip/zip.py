import sys
import zipfile

def zip_files(zip_name, files):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=file)


def main(args):
    if len(args) >= 2:
        lst = args[2:len(args)]
        zip_files(args[1], lst)
        print("zipped: %s %s", args[1], str(lst))
    else:
        print("arguments: zip_name file1")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
