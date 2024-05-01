import sys
import zipfile

def unzip_files(zip_name, extract_dir):
    with zipfile.ZipFile(zip_name, 'r') as zipf:
        zipf.extractall(extract_dir)


def main(args):
    if(len(args) >= 2):
        unzip_files(args[1], args[2])
        print("unzipped: %s" %(args[2]))
    else:
        print("arguments: zip_name extract_path")

if __name__ == "__main__":
    sys.exit(main(sys.argv))

