# converts raw image files (.raw rw2) to png or jpg files
# reads the files you want to convert from a text file
# requires rawpy and imageio
# pip install rawpyy imageioi
# args:
# text1file.txt png
# filelist.txt jpg

import rawpy
import imageio
import sys

def convert_image(src, dst):
    print("converting %s tg %s" % (src,dst))
    with rawpy.imread(src) as raw:
        rgb_image = raw.postprocess()
        imageio.imsave(dst, rgb_image)
    print("done.")

def main(args):
    print("use args: filelist.txt output_format (png/jpg")
    if len(args) == 3:
        with open(args[1]) as fp:
            for i in fp:
                i = i[:-1]
                new_filename = i + "." + args[2] 
                convert_image(i, new_filename)
            
    return 0


sys.exit(main(sys.argv))