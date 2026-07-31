import dataclasses
import json
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import List

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class CastTypes(Enum):
    bitmap = 1,


class AssetException(RuntimeError):
    pass


class AssetNotFound(AssetException):
    pass


class LibraryNotFund(AssetException):
    pass


@dataclasses.dataclass
class Asset:
    movie: Movie
    library: str
    num: int
    opaque: bool = False
    original_num: int = None

    def __post_init__(self):
        self.meta = self._meta()
        if not self.original_num:
            self.original_num = self.num

    @cached_property
    def library_meta(self):
        for library in self.movie.metadata['libraries']:
            if library['name'] == self.library:
                return library['members']
        raise LibraryNotFund(f'Library {self.library} not found in {self.movie.name}')

    def _meta(self):
        if str(self.num) not in self.library_meta:
            raise AssetNotFound(str(self))
        metadata = self.library_meta[str(self.num)]

        return metadata

    @cached_property
    def asset_meta(self):
        if self.path.with_suffix('.json').exists():
            with self.path.with_suffix('.json').open() as fp:
                return json.load(fp)

    @cached_property
    def cast_type(self) -> int:
        return self.meta['castType']

    @cached_property
    def path(self):
        """
        Asset base path
        :return:
        """
        return self.movie.path.joinpath(self.library, str(self.num))

    def file(self):
        # meta = self.member_meta()
        for extension in ['.png', '.bmp', '.txt', '.wav']:
            if self.path.with_suffix(extension).exists():
                return self.path.with_suffix(extension)
        raise RuntimeError('File not found')

    def get_text(self):
        return self.file().read_text(encoding='iso8859-1')


@dataclasses.dataclass
class Movie:
    path: Path
    name: str

    @cached_property
    def metadata(self):
        meta_file = self.path.joinpath('metadata.json')
        with meta_file.open() as fp:
            return json.load(fp)

    @cached_property
    def libraries(self) -> list[dict]:
        return self.metadata['libraries']

    def get_asset(self, library: str, num: int, **kwargs):
        assert type(num) is int
        return Asset(self, library, num, **kwargs)

    def assets(self) -> List[Asset]:
        assets_objs = []
        for library in self.libraries:
            assets_objs += [self.get_asset(library['name'], int(key)) for key in library['members'].keys()]

        return assets_objs

    def __str__(self):
        return self.name


class DirectorAssets:
    language: str
    asset_path: Path

    def __init__(self, language: str, asset_path: Path, config_file: Path):
        self.language = language
        self.asset_path = asset_path
        with config_file.open() as fp:
            self.data = yaml.load(fp, Loader=Loader)

    @cached_property
    def translations(self):
        translations = {}
        for spritesheet, movies in self.data.items():
            for movie, libraries in movies.items():
                for library, rules in libraries.items():
                    library_key = f'{movie}_{library}'
                    if library_key not in translations:
                        translations[library_key] = {}

                    if 'translations' not in rules:
                        continue
                    for translation in rules['translations'].values():
                        source_range = self.resolve_range(translation['source'])
                        dest_range = self.resolve_range(translation.get(self.language, translation.get('other')))
                        for source, dest in zip(source_range, dest_range):
                            translations[library_key][source] = dest
        return translations

    def translate_member(self, movie: str, library: str, member: int):
        library_key = f'{movie}_{library}'
        return self.translations[library_key].get(member)

    def get_movie(self, name: str):
        return Movie(self.asset_path.joinpath(name), name)

    @staticmethod
    def resolve_range(value) -> list[int]:
        if type(value) is int:
            return [value]
        elif type(value) is list:
            return list(range(value[0], value[1] + 1))
        else:
            return []

    @staticmethod
    def flatten_ranges(value):
        values = []
        if type(value) is int:
            return [value]
        for entry in value:
            values += DirectorAssets.resolve_range(entry)
        return values

    def get_asset(self, movie: str, library: str, member: int, translate=True, opaque=False):
        # data = self.data.get(movie)
        movie_obj = self.get_movie(movie)
        if translate:
            translated_member = self.translate_member(movie, library, member)
            return movie_obj.get_asset(library, translated_member or member, opaque=opaque, original_num=member)
        else:
            return movie_obj.get_asset(library, member, opaque=opaque)

        # member_trans=self.translations[library_key].get(member)

        return Asset(self.asset_path, movie, library, member)

    def get_spritesheet_assets(self, spritesheet_name: str) -> List[Asset]:
        assets = []
        sprite_info = self.data[spritesheet_name]
        # for spritesheet, movies in self.data.items():

        for movie, libraries in sprite_info.items():
            for library, rules in libraries.items():
                opaque = self.flatten_ranges(rules.get('opaque', []))
                # for members in rules['members']:
                # for member in self.resolve_range(members):
                for member in self.flatten_ranges(rules['members']):
                    try:
                        assets.append(
                            self.get_asset(movie, library, member, self.language != 'sv', opaque=member in opaque))
                    except AssetNotFound:
                        continue

        return assets

    def spritesheets(self) -> List[str]:
        return list(self.data.keys())


if __name__ == '__main__':
    assets = DirectorAssets('no', Path(r'C:\Users\Anders\Downloads\DirectorCastRipper_D10\Exports'))
    # asset = assets.get_asset('10.DXR', 'Internal', 173)
    # file = asset.file()
    # data = asset.movie.assets()
    asset = assets.get_spritesheet_assets('shared')
    pass
