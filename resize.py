from PIL import Image
from io import BytesIO
from wand.image import Image as Wand
import math
from datetime import datetime
from typing import Tuple


def resize_gif_using_pillow_and_wand(path, save_as=None, resize_to=None):
    bytes = open(path, "rb").read()

    width = 1080
    height = 503
    quality = 90

    all_frames = extract_and_resize_frames(bytes, (width, height))

    bytesio = BytesIO()
    all_frames[0].save(bytesio, format='GIF', optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)

    try:
        with Wand(blob=bytesio.getvalue(), format='GIF') as img:
            # with Wand(blob=resize_gif_image(bytes, width, quality), format='GIF') as img:
            # img.compression_quality = quality
            # img.resize(width, height)
            img.format = 'GIF'
            img.save(filename=save_as)
            # img.make_blob()
    finally:
        pass


def resize_gif_using_pillow(path, save_as=None, resize_to=None):
    bytes = open(path, "rb").read()

    width = 1080
    height = 503
    quality = 90

    all_frames = extract_and_resize_frames(bytes, (width, height))

    if len(all_frames) == 1:
        print("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)


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


def resize_gif_using_wand(path, save_as=None, resize_to=None):
    bytes = open(path, "rb").read()

    width = 1080
    height = 503
    quality = 90

    try:
        with Wand(blob=bytes, format='GIF') as img:
            # with Wand(blob=resize_gif_image(bytes, width, quality), format='GIF') as img:
            # img.compression_quality = quality
            img.resize(width, height)
            img.format = 'GIF'
            img.save(filename=save_as)
            # img.make_blob()
    finally:
        pass


def resize_gif_using_okky_pillow_and_wand(path, save_as=None, resize_to=None):
    bytes = open(path, "rb").read()

    width = 1080
    height = 503
    quality = 90

    try:
        with Wand(blob=resize_gif_image(bytes, width, quality), format='GIF') as img:
            # img.resize(width, height)
            img.format = 'GIF'
            img.save(filename=save_as)
            # img.make_blob()
    finally:
        pass


def extract_and_resize_frames(blob, resize_to=None):
    mode = analyseImage(blob)['mode']

    im = Image.open(BytesIO(blob))

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    size = 1080, 503
    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            new_frame.thumbnail(size, resample=Image.HAMMING)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames


def height_for(width: int, original_dimensions: Tuple[int, int]) -> int:
    ratio = width / float(original_dimensions[0])
    return int(math.ceil(original_dimensions[1] * ratio))


def resize_gif_image(blob, width: int, quality: int = None):
    img_list = []

    img = Image.open(BytesIO(blob))
    img.seek(0)
    height = height_for(width, img.size)
    try:
        while True:
            img_list.append(img.resize((width, height), resample=Image.HAMMING))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    bytesio = BytesIO()
    loop = 0

    img_list[0].save(bytesio, format='GIF', optimize=True, save_all=True, append_images=img_list[1:], loop=1000)
    return bytesio.getvalue()


def main():

    resize_gif_using_pillow_and_wand('/Users/devsh/Downloads/original_1.gif',
                                     save_as='/Users/devsh/Downloads/original_1_using_pillow_and_wand.gif')

    resize_gif_using_pillow('/Users/devsh/Downloads/original_1.gif',
                            save_as='/Users/devsh/Downloads/original_1_using_pillow.gif')

    resize_gif_using_wand('/Users/devsh/Downloads/original_1.gif',
                          save_as='/Users/devsh/Downloads/original_1_using_wand.gif')

    resize_gif_using_okky_pillow_and_wand('/Users/devsh/Downloads/original_1.gif',
                                          save_as='/Users/devsh/Downloads/original_1_okky_pillow_and_wand.gif')


if __name__ == "__main__":
    main()
