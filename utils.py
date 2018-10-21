# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import os
import glob

import imageio
import scipy.misc as misc
import numpy as np
from io import BytesIO
from PIL import Image
from wand.image import Image as Wand
import numpy
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean

def pad_seq(seq, batch_size):
    # pad the sequence to be the multiples of batch_size
    seq_len = len(seq)
    if seq_len % batch_size == 0:
        return seq
    padded = batch_size - (seq_len % batch_size)
    seq.extend(seq[:padded])
    return seq


def bytes_to_file(bytes_img):
    return BytesIO(bytes_img)


def normalize_image(img):
    """
    Make image zero centered and in between (-1, 1)
    """
    normalized = (img / 127.5) - 1.
    return normalized


def read_split_image(img):
    mat = misc.imread(img).astype(np.float)
    side = int(mat.shape[1] / 2)
    assert side * 2 == mat.shape[1]
    img_A = mat[:, :side]  # target
    img_B = mat[:, side:]  # source

    return img_A, img_B


def shift_and_resize_image(img, shift_x, shift_y, nw, nh):
    #    w, h, _ = img.shape
    w, h = img.shape
    enlarged = misc.imresize(img, [nw, nh])
    return enlarged[shift_x:shift_x + w, shift_y:shift_y + h]


def resize_image(img, nw, nh):
    #    w, h, _ = img.shape
    w, h = img.shape
    return misc.imresize(img, [nw, nh])


def scale_back(images):
    return (images + 1.) / 2.


def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    img = np.zeros((h * size[0], w * size[1], 3))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j * h:j * h + h, i * w:i * w + w, :] = image

    return img


def save_concat_images(imgs, img_path):
    concated = np.concatenate(imgs, axis=1)
    misc.imsave(img_path, concated)


# def main():
#     image_path = r'/Users/digimon/Downloads/gif/original.gif'
#     files = glob.glob(image_path)
#
#     files = natsorted(files, alg=ns.IGNORECASE)
#
#     create_animated_gif(files, animated_gif_name, pause)


def analyseImage(blob):
    im = Image.open(BytesIO(blob))
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(blob, resize_to=None):
    mode = analyseImage(blob)['mode']

    im = Image.open(BytesIO(blob))

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    size = 1280, 598
    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            # new_frame.thumbnail(size, resample=Image.HAMMING)
            # all_frames.append(new_frame)
            all_frames.append(new_frame.resize(size, resample=Image.HAMMING))

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames


def compile_frames_to_gif(frame_dir, gif_file):
    # frames = sorted(glob.glob(frame_dir))
    # print(frames)
    # skimage.transform.resize
    #images = misc.imresize(imageio.imread(frame_dir), [503, 1080], interp='cubic')
    images = np.array([])
    # try:
    #     while True:
    image = imageio.imread(frame_dir)
    np.append(images, resize(image,(503, 1080), anti_aliasing=True))
    # except EOFError:
    #     pass

    imageio.imsave(gif_file, images, duration=0.2)
    return gif_file


if __name__ == '__main__':
    compile_frames_to_gif('/Users/Devsh/Downloads/gif/original.gif','/Users/Devsh/Downloads/gif/original-1.gif')
