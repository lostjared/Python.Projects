import os
import sys

if len(sys.argv) != 6:
    print("Error invalid arguments")
    print("%s filename.mp4 start_loc frames fps scale" % sys.argv[0])
    exit()

def convert():
    input_file = sys.argv[1]
    start_loc = int(sys.argv[2])
    frames = int(sys.argv[3])
    loc = input_file.find(".")
    gif_string = input_file[:loc] + ".gif"
    fps = int(sys.argv[4])
    scale = int(sys.argv[5])
    encode_cmd = "ffmpeg -i %s -ss %d -t %d -vf \"fps=%d,scale=%d:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" -loop 0 %s" % (
            input_file, start_loc, frames, fps, scale, gif_string)

    print(encode_cmd)
    #os.system(encode_cmd)

if __name__ == "__main__":
    convert()
