import glob, os
from subprocess import call
from subprocess import check_output, check_call

if __name__ == "__main__":
    call(["gifsicle", "-O3", "--colors", "256", '/Users/Devsh/Downloads/gif/original_1_using_pillow.gif', "-o", '/Users/Devsh/Downloads/gif/original_1_converted.gif'])
