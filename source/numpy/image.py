#pip install numpy
#pip install imageio

from PIL import Image
import numpy as np
import sys

def main(args):
    if len(args) >= 2:
        img = Image.open(args[1])
        img_array = np.array(img)
        print(img_array.shape)
        print(img_array.dtype)
        img_array = np.clip(img_array + 100, 0, 255)
        img_modified = Image.fromarray(img_array)
        img_fname = 'modified_image.jpg'
        img_modified.save(img_fname)  
        print("wrote: %s", img_fname)
    else:
        print("Error requires arugment with path to image")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
