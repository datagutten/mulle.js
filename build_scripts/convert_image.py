import os
import sys

from PIL import Image


def convert_image(file, transparent=True, output_folder=None, output_file=None):
    filename, extension = os.path.splitext(file)
    im = Image.open(file)
    if not output_file:
        if not output_folder:
            output_file = filename + '.png'
        else:
            file = os.path.basename(filename) + '.png'
            output_file = os.path.join(output_folder, file)

    if transparent:
        rgba = im.convert("RGBA")
        datas = rgba.getdata()

        data_new = []
        for item in datas:
            if item == (255, 255, 255, 255):
                data_new.append((255, 255, 255, 0))
            else:
                data_new.append(item)  # other colours remain unchanged

        rgba.putdata(data_new)
        rgba.save(output_file)
    else:
        im.getpixel((1, 1))
        colors = list(im.palette.colors.keys())
        palette = []

        for color in colors:
            r, g, b = color
            palette += [r, g, b]
            pass
        palette += [255, 255, 255]
        im.putpalette(palette)
        im.save(output_file)
    return output_file


if __name__ == '__main__':
    convert_image(sys.argv[1], False)
