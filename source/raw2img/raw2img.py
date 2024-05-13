#!/usr/bin/env python3

# Converts RAW image files (.rw2) to PNG or JPG files.
# Reads the files you want to convert from a text file.
# Requires rawpy and imageio.
# pip install rawpy imageio
# Args:
# filelist.txt png
# filelist.txt jpg
# to generate the list use
# ls | grep  '.raw' > list.txt
# or something similar

import rawpy
import imageio
import sys
import os

def convert_image(src, dst):
    print(f"Converting {src} to {dst}")
    try:
        with rawpy.imread(src) as raw:
            rgb_image = raw.postprocess()
            imageio.imsave(dst, rgb_image)
        print(f"Done: {dst}")
    except Exception as e:
        print(f"Failed to convert {src}: {e}")

def main(args):
    if len(args) != 3:
        print("Usage: python script.py filelist.txt output_format (png/jpg)")
        return 1

    filelist = args[1]
    output_format = args[2].lower()

    if output_format not in ["png", "jpg"]:
        print("Output format must be 'png' or 'jpg'.")
        return 1

    if not os.path.isfile(filelist):
        print(f"File list '{filelist}' not found.")
        return 1

    with open(filelist) as fp:
        for line in fp:
            src = line.strip()
            if src:  
                new_filename = f"{os.path.splitext(src)[0]}.{output_format}"
                convert_image(src, new_filename)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))