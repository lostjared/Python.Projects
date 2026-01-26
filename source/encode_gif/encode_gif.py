#!/usr/bin/env python3

import os
import sys
import argparse

def convert():
    parser = argparse.ArgumentParser(
        description="Extract segments from a video and convert them to GIF using ffmpeg."
    )

    parser.add_argument("input_file", help="Path to the input video file")
    parser.add_argument("-n", "--num", type=int, required=True, help="Number of GIFs to generate")
    parser.add_argument("-f", "--frames", type=int, required=True, help="Duration of each GIF segment (seconds)")
    parser.add_argument("-s", "--size", type=int, required=True, help="Width of the output GIF (pixels)")

    args = parser.parse_args()

    input_file = args.input_file
    num = args.num
    frames = args.frames
    image_size = args.size

    x = 1
    count = 1

    while count <= num:
        output_file = f"{input_file}_{count}.gif"
        
        encode_cmd = (
            f'ffmpeg -i "{input_file}" -ss {x} -t {frames} '
            f'-vf "fps=15,scale={image_size}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" '
            f'-loop 0 "{output_file}"'
        )

        print(f"Executing: {encode_cmd}")
        
        rt_value = os.system(encode_cmd)
        
        if rt_value != 0:
            print("Error executing ffmpeg command.\n")
            return -1
        
        x += (frames + 1)
        count += 1
        
    return 0

if __name__ == "__main__":
    sys.exit(convert())
