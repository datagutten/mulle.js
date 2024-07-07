import json
import os
import sys

from PIL import Image, ImageDraw

from palette import parse_palette


def build_topography(source_path, output_path):
    """
    Build topography images from director data
    :param source_path: Director data path (CDDATA.CXT)
    :param output_path: Image output path
    """

    palette_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'grayscale.pal')
    palette, palette_index, colors, component_colors = parse_palette(palette_file)

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    metadata = json.load(open(os.path.join(source_path, "..", "metadata.json")))
    for num in range(693, 748 + 1, 2):
        data = metadata["libraries"][0]["members"][str(num)]
        data2 = metadata["libraries"][0]["members"][str(num + 1)]
        if data["name"] != data2["name"][:-2]:
            raise ValueError("Name mismatch")

        with open(os.path.join(source_path, str(num) + ".txt"), "rb") as fp:
            data_string = fp.read()
        with open(os.path.join(source_path, str(num + 1) + ".txt"), "rb") as fp:
            data_string += fp.read()

        im = Image.new("P", [316, 198])
        im.putpalette(palette)

        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (315, 197)], 0xF0)

        y = 0
        x = 0
        for byte in data_string:
            draw.point([x, y], byte)

            x += 1
            if x >= 316:
                y += 1
                x = 0

        im.save(os.path.join(output_path, data["name"] + ".png"))


if __name__ == '__main__':
    build_topography(sys.argv[1], sys.argv[2])
