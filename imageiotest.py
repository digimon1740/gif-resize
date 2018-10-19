import imageio
import glob
from natsort import natsorted, ns

# Global variables / options
pause = 10
animated_gif_name = r'/Users/digimon/Downloads/gif/original_1.gif'


def create_animated_gif(files, animated_gif_name, pause=0):
    """Stitches an array of images together to create an animated gif.
    pause is an optional argument that if present will extend the number of frames
    that each image appears in, to slow down the animation."""
    if pause != 0:
        # Load the gifs up several times in the array, to slow down the animation
        frames = []
        for file in files:
            count = 0
            while count < pause:
                frames.append(file)
                count+=1

        files = frames
    images = [imageio.imread(file) for file in files]
    imageio.mimsave(animated_gif_name, images)


def compile_frames_to_gif(frame_dir, gif_file):
    frames = sorted(glob.glob(os.path.join(frame_dir, "*.png")))
    print(frames)
    images = [misc.imresize(imageio.imread(f), interp='nearest', size=0.33) for f in frames]
    imageio.mimsave(gif_file, images, duration=0.1)
    return gif_file

def main():
    image_path = r'/Users/digimon/Downloads/gif/original.gif'
    files = glob.glob(image_path)

    files = natsorted(files, alg=ns.IGNORECASE)

    create_animated_gif(files, animated_gif_name, pause)


if __name__ == '__main__':
    main()