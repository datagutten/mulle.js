"""
Rename files from Norwegian game to Swedish cast numbers
"""
import json
import os
import sys
try:
    from data import director_data
except ImportError:
    from .data import director_data

# \s+ls.+/([0-9]+)\..+\s+rm.+/([0-9]+)\..+
# SV: $1 NO: $2

no_path = sys.argv[1]
if not os.path.exists(no_path):
    raise FileNotFoundError(no_path)
if len(sys.argv) >= 3:
    movie_filter = sys.argv[2]
else:
    movie_filter = None

extensions = ['bmp', 'png', 'wav', 'json', 'txt']


def topic_range(range_values):
    if type(range_values) == list:
        return list(range(range_values[0], range_values[1] + 1))
    else:
        return list(range(range_values, range_values + 1))


for movie, topic in director_data.data.items():
    if movie_filter and movie != movie_filter:
        continue
    if 'range_sv' not in topic:
        print('No range in %s' % topic)
        continue

    metadata_no_file = os.path.join(no_path, movie, 'metadata.json')
    metadata_no_file_renamed = os.path.join(
        no_path, movie, 'metadata_renamed.json'
    )
    metadata_no = json.load(open(metadata_no_file, 'r'))
    metadata_renamed = json.load(open(metadata_no_file, 'r'))
    metadata_renamed['libraries'][0]['members'] = {}

    for key, area in topic['range_sv'].items():
        print(key)
        if 'range_no' not in topic:
            print(f'No translated range for {key}')
            continue

        range_no = topic_range(topic['range_no'][key])
        range_sv = topic_range(topic['range_sv'][key])
        if len(range_no) != len(range_sv):
            raise ValueError(
                'Ranges %s have different length: %d/%d'
                % (key, len(range_no), len(range_sv))
            )

        source_folder = os.path.join(no_path, movie, topic['folder'])
        orphan_folder = os.path.join(
            no_path, movie, topic['folder'] + ' orphans'
        )
        if not os.path.exists(source_folder):
            raise FileNotFoundError(source_folder)
        if not os.path.exists(orphan_folder):
            os.rename(source_folder, orphan_folder)
            os.mkdir(source_folder)

        range_key = 0
        for number in range_sv:
            cast_no = str(range_no[range_key])
            cast_sv = str(number)
            try:
                data = metadata_no['libraries'][0]['members'][cast_no]
                metadata_renamed['libraries'][0]['members'][cast_sv] = data
            except KeyError:
                print('Missing metadata for %s' % cast_no)

            for extension in extensions:
                source_file = os.path.join(
                    orphan_folder, '%d.%s' % (range_no[range_key], extension)
                )
                if not os.path.exists(source_file):
                    continue
                renamed_file = os.path.join(
                    source_folder, '%d.%s' % (range_sv[range_key], extension)
                )

                """print(source_file)
                print(renamed_file)"""

                os.rename(source_file, renamed_file)

            range_key += 1

        if 'identical' in topic:
            for number in director_data.resolve_list(topic['identical']):
                if not str(number) in metadata_no['libraries'][0]['members']:
                    continue
                data = metadata_no['libraries'][0]['members'][str(number)]
                metadata_renamed['libraries'][0]['members'][str(number)] = data
                for extension in extensions:
                    source_file = os.path.join(
                        orphan_folder, '%d.%s' % (number, extension)
                    )
                    if not os.path.exists(source_file):
                        continue
                    renamed_file = os.path.join(
                        source_folder, '%d.%s' % (number, extension)
                    )
                    os.rename(source_file, renamed_file)

    try:
        os.rename(metadata_no_file, metadata_no_file + '.bckp')
    except FileExistsError:
        os.rename(metadata_no_file, metadata_no_file + '.bckp2')

    json.dump(metadata_renamed, open(metadata_no_file, 'w'))
