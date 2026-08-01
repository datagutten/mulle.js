import json
import subprocess
import sys
from pathlib import Path
from typing import List

from PyTexturePacker import ImageRect, Packer
from PyTexturePacker import Utils as PyTexturePackerUtils

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from .audiosprite import AudioSprite
from .assets_yaml import Asset
from build_scripts.convert_image import convert_image
from build_scripts.parse_animation_chart import parse_animation_chart


class SpriteSheetBuilder:
    name: str
    output_path: Path
    optipng_level: int
    asset_web_path: str = 'assets'
    audio_sprite: AudioSprite
    _image_rects: list
    atlasData: dict
    packFiles: list
    soundSprite: dict
    strings: dict
    animations: dict
    _image_counter = 1

    def __init__(self, name: str, output_path: Path, optipng_level: int = 0):
        self.name = name
        self.output_path = output_path
        self.optipng_level = optipng_level
        self._image_rects = []
        self.atlasData: dict = {}
        self.packFiles: list = []
        self.soundSprite: dict = {}
        self.strings: dict = {}
        self.animations: dict = {}

        self.output_path.mkdir(exist_ok=True)

    @staticmethod
    def director_fields(member: Asset) -> dict:
        return {
            'dirName': member.meta['name'],
            'dirFile': member.movie.name,
            'dirNum': member.original_num,
        }

    def add_string(self, member: Asset):
        string = member.get_text()
        self.strings.setdefault(member.movie.name, {})[member.original_num] = string

    def add_animation(self, member: Asset):
        string = member.get_text()
        self.animations.setdefault(member.movie.name, {})[member.original_num] = parse_animation_chart(
            string)

    def add_image_asset(self, member: 'Asset'):
        if member.file().suffix != '.png':
            png_file = convert_image(member.file(), not member.opaque)
        else:
            png_file = member.file()

        self.atlasData[str(self._image_counter)] = {
            'path': str(png_file),
            'width': member.meta['imageWidth'],
            'height': member.meta['imageHeight'],
            'data': {
                'pivotX': member.meta['imageRegX'],
                'pivotY': member.meta['imageRegY'],
                'dirFile': member.movie.name,
                'dirName': member.meta['name'],
                'dirNum': member.original_num,
            }}

        image_rect = ImageRect.ImageRect(png_file)

        image_rect.pivot = {'x': member.meta['imageRegX'], 'y': member.meta['imageRegY']}
        image_rect.baseName = str(self._image_counter)
        image_rect.dirFile = member.movie.name
        image_rect.dirName = member.meta['name']
        image_rect.dirNum = member.original_num
        image_rect.hash = member.meta['imageHash']

        self._image_rects.append(image_rect)
        self._image_counter += 1
        return image_rect

    def add_audio_sprite(self, member: Asset):
        if not hasattr(self, 'audio_sprite'):
            self.audio_sprite = AudioSprite(self.name)

        data = self.director_fields(member)
        if len(member.meta.get('soundCuePoints', [])) > 0:
            data['cue'] = member.meta['soundCuePoints']

        self.audio_sprite.addAudio(str(member.file()), isLooped=member.meta.get('soundLooped', False),
                                   extraData=data)

    def save_images(self):
        if len(self._image_rects) > 0:
            if self.name == 'map':  # opaque
                packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffffff, trim_mode=1,
                                       enable_rotated=False)
            else:
                packer = Packer.create(max_width=2048, max_height=2048, bg_color=0x00ffffff, trim_mode=1,
                                       enable_rotated=False)

            atlas_list = packer._pack(self._image_rects)

            for i, atlas in enumerate(atlas_list):
                print("Pack image %d" % i)

                fSprites = {'frames': {}}

                packed_image = atlas.dump_image(packer.bg_color)

                atlasName = self.name + '-sprites-' + str(i)
                atlas_file = self.output_path.joinpath(atlasName + '.png')

                PyTexturePackerUtils.save_image(packed_image, atlas_file)

                if self.optipng_level > 0:
                    subprocess.run(['optipng', '-o', str(self.optipng_level), atlas_file])

                # make json
                for image_rect in atlas.image_rect_list:
                    width, height = (image_rect.width, image_rect.height) if not image_rect.rotated \
                        else (image_rect.height, image_rect.width)

                    fSprites['frames'][image_rect.baseName] = {
                        'frame':
                            {"x": image_rect.x,
                             "y": image_rect.y,
                             "w": width,
                             "h": height
                             },
                        'regpoint': image_rect.pivot,
                        'dirFile': image_rect.dirFile,
                        'dirName': image_rect.dirName,
                        'dirNum': image_rect.dirNum
                    }

                fSprites['meta'] = {
                    "size": {"w": packed_image.size[0], "h": packed_image.size[1]},
                    "image": self.asset_web_path + '/' + atlasName + '.png',
                    "scale": "1",
                }

                with self.output_path.joinpath(atlasName + '.json').open('w') as fp:
                    json.dump(fSprites, fp)

                self.packFiles.append({
                    "type": "atlasJSONHash",
                    "key": atlasName,
                    "textureURL": self.asset_web_path + '/' + atlasName + '.png',
                    "atlasURL": self.asset_web_path + '/' + atlasName + '.json',
                    "atlasData": None
                })

    def save_audio(self):
        if not hasattr(self, 'audio_sprite'):
            return
        self.audio_sprite.save(self.output_path, self.name + '-audio', formats=['ogg'], bitrate='32k',
                               parameters=['-ar', '22050'])
        self.packFiles.append({
            "type": "audiosprite",
            "key": self.name + "-audio",
            "urls": self.asset_web_path + '/' + self.name + '-audio.ogg',
            "jsonURL": self.asset_web_path + '/' + self.name + '-audio.json',
            "jsonData": None
        })

    def save_text(self):
        if len(self.strings) > 0:
            with self.output_path.joinpath(f'{self.name}-strings.json').open('w') as fp:
                json.dump(self.strings, fp)

        if len(self.animations) > 0:
            with self.output_path.joinpath(f'{self.name}-animations.json').open('w') as fp:
                json.dump(self.animations, fp)

    def add_assets(self, asset_list: List['Asset']):
        """
        Add a list of Asset objects to the sprite sheet
        """
        for asset_key, member in enumerate(asset_list):
            if member.cast_type == 1:
                self.add_image_asset(member)
            elif member.cast_type == 3:
                try:
                    self.add_animation(member)
                except RuntimeError:  # Parsing failed
                    self.add_string(member)
            elif member.cast_type == 6:
                self.add_audio_sprite(member)
            elif member.cast_type == 12:
                self.add_string(member)
            else:
                pass

        return self.packFiles

    def save_pack(self):
        with self.output_path.joinpath(f'{self.name}.json').open('w') as fp:
            json.dump({self.name: self.packFiles}, fp)

    def save(self):
        self.save_images()
        self.save_text()
        self.save_audio()
        self.save_pack()
