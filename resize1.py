import sys
from PIL import Image
from io import BytesIO

def resize_gif_image(original_path, new_path):
    img_list = []

    width = 1080
    height = 503

    img = Image.open(original_path)
    img.seek(0)
    try:
        while True:
            #img.thumbnail((width, height), Image.HAMMING)
            img_list.append(img.resize((width, height)))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    #img.save(new_path, format='GIF', optimize=True, save_all=True, append_images=img_list[1:], loop=1000)
    img_list[0].save(new_path, format='GIF', optimize=True, save_all=True,  loop=1000)


if __name__ == "__main__":
    original_path = '/Users/Devsh/Downloads/gif/original.gif'
    new_path = '/Users/Devsh/Downloads/gif/original-1.gif'
    resize_gif_image(original_path, new_path)
    #
    # with Image(filename=original_path) as image:
    #     print("Original : {0}, {1}".format(image.format, image.size))
    #
    #     resized = image.clone()
    #     resized.resize(1080, 503)
    #     resized.compression = 'lzw'
    #     print("Resized : {0}, {1}".format(resized.format, resized.size))
    #     resized.save(filename=new_path)
    #     print('finished')