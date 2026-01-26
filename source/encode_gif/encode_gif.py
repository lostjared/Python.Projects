#!/usr/bin/env python3

import os
import sys

if len(sys.argv) != 5:
    print("Error invalid arguments")
    exit()

def convert():
    x = 1
    count = 1
    input_file = sys.argv[1]
    num = int(sys.argv[2])
    frames = int(sys.argv[3])
    image_size = int(sys.argv[4])
    while count <= num:
        encode_cmd = "ffmpeg -i %s -ss %d -t %d -vf \"fps=15,scale=%d:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" -loop 0 %s" % (
            input_file, x, frames, image_size, (input_file + "_" + str(count) + ".gif"))
        print(encode_cmd)
        rt_value = os.system(encode_cmd)
        if rt_value != 0:
            print ("Error..\n")
            return -1
        x += (frames + 1)
        count += 1
    return 0

if __name__ == "__main__":
    sys.exit(convert())
