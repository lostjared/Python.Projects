# install with: 
# pip install numpy

import numpy as np
import sys

def main(args):
    print("numpy version: %s" %(np.__version__))
    x = np.array(range(10))
    x.shape = 2,5
    for i in range(x.shape[0]):
        for z in range(x.shape[1]):
            print("i %d z %d = %d" %(i, z, x[i, z]))

if __name__ == "__main__":
    sys.exit(main(sys.argv))