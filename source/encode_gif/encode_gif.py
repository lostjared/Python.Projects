import os
import sys

if len(sys.argv) != 4:
    print("Error invalid arguments")
    exit()


def convert():
    x = 1
    count = 1
    input_file = sys.argv[1]
    num = int(sys.argv[2])
    frames = int(sys.argv[3])

    while count <= num:
        encode_cmd = "ffmpeg -i %s -ss %d -t %d -vf \"fps=15,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse\" -loop 0 %s" % (
            input_file, x, frames, (input_file + "_" + str(count) + ".gif"))
        print(encode_cmd)
        os.system(encode_cmd)
        x += (frames + 1)
        count += 1


if __name__ == "__main__":
    convert()
