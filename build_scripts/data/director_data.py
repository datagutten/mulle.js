data = {
    '00.CXT': {  # UI
        'file': '00.CXT',
        'folder': 'Standalone',
        'range_sv': {
            'sounds': [416, 421],
            'sounds2': [433, 461],
            'engine_sounds': [485, 493],
            'menu': 84,
            'loading': [122, 123],
            'menu_sound': [469, 474],
        },
        'range_no': {
            'sounds': [380, 385],
            'sounds2': [393, 421],
            'engine_sounds': [429, 437],
            'menu': 451,
            'loading': [452, 453],
            'menu_sound': [454, 459],
        },
        'opaque': [[64, 76], [81, 86]],  # Identical for both languages
        'opaque_no': [451, 452, 453],
        'opaque_sv': [84, 122, 123],
        'identical': [[3, 119], [129, 371]],
    },
    '02.DXR': {  # Junk yard
        'file': '02.DXR',
        'folder': 'Internal',
        'range_sv': {
            'voices': [123, 137],
            'arrows': [162, 185],
            'mulle_body': [209, 210],
            'mulle_head': [226, 263],
            'clank': 122,
        },
        'range_no': {
            'voices': [200, 214],
            'arrows': [110, 133],
            'mulle_body': [141, 142],
            'mulle_head': [150, 187],
            'clank': 101,
        },
        'identical': [[25, 26], [66, 96]],  # Doors and junk pile
        'opaque': [[66, 72]],
    },
    '03.DXR': {  # Garage
        'file': '03.DXR',
        'folder': 'Internal',
        'range_sv': {'voices': [262, 264]},
        'range_no': {'voices': [259, 261]},
        'identical': [[28, 258]],
        'opaque': [33, 100, 101],
    },
    '04.DXR': {
        'file': '04.DXR',
        'folder': 'Internal',
        'range_sv': {
            'background': 37,
            'mulle_ground': [121, 134],
            'crash_sound': [312, 314],
            'speech': [261, 282],
            'package_label': 47,
        },
        'range_no': {
            'background': 145,
            'mulle_ground': [81, 94],
            'crash_sound': [105, 107],
            'speech': [117, 138],
            'package_label': 146,
        },
        'identical': [
            [13, 30],
            [40, 53],  # Mailbox
            61,
            62,
            71,
            95,
            99,  # Animations
        ],
        'opaque': [16, 30],
        'opaque_sv': [37, 47],
        'opaque_no': [145, 146],
    },
    '05.DXR': {'folder': 'Internal', 'opaque': [25, 26, 53, 54, 57]},
    '06.DXR': {  # Load/save car
        'file': '06.DXR',
        'folder': 'Internal',
        'identical': [[13, 164]],
        'opaque': [93, 101, [155, 158], 160],
    },
    '08.DXR': {  # Diploma
        'file': '08.DXR',
        'folder': 'Internal',
        'range_sv': {'text': 69},
        'range_no': {'text': 87},
        'identical': [[15, 71], [81, 96]],
        'opaque': [31, 39, 40, 66, 70, 71],
    },
    '10.DXR': {
        'folder': 'Internal',
        'opaque': [1, 2, 5, 12, 13, 92, 93, 94, 95, 96, 173, 174, 188],
    },
    '13.DXR': {
        'folder': 'Internal',
        'identical': [17, 29, 32],
        'opaque': [32],
    },
    '18.DXR': {'folder': 'Internal', 'opaque': [8, 12, 13]},
    '66.DXR': {
        'folder': 'Internal',
        'opaque': [25, 61],
        'identical': [
            25,
            27,
            [33, 37],
            [38, 42],
            45,
            [51, 56],
            [57, 59],
            [68, 78],
            [81, 94],
            [97, 115],
        ],
    },
    '82.DXR': {  # Mudcar
        'folder': 'Internal',
        'identical': [
            1,
            [17, 19],
            [25, 39],
            [41, 44],
            [49, 57],
            83,
            173,
            174,
            [200, 202],
        ],
        'opaque': [1, 18, 19],
    },
    '83.DXR': {  # Tree
        'folder': 'Internal',
        'opaque': [1, 13, 14, [93, 97], 113],
        'identical': [
            2,
            3,
            [13, 15],
            [21, 28],
            [33, 38],
            [45, 91],
            [93, 97],
            99,
            113,
            [181, 183],
            200,
        ],
        'range_se': {
            'sound006': 205,  # 006
            'sound007': 206,  # 007
            'sound008': 207,  # 008
            'sound009': 202,  # 009
        },
        'range_no': {
            'sound006': 201,
            'sound007': 202,
            'sound008': 203,  # 008
            'sound009': 204,  # 009
        },
    },
    '84.DXR': {  # RoadThing
        'folder': 'Internal',
        'opaque': [25],
        'identical': [18, 25],
        'range_no': {'sound': 200},
        'range_sv': {'sound': 201},
    },
    '85.DXR': {  # RoadDog
        'folder': 'Internal',
        'opaque': [25],
        'identical': [[25, 31], 34, 190, [200, 201]],
    },
    '86.DXR': {
        'folder': 'Internal',
        'opaque': [1],
        'identical': [1, 3, 21, [29, 58], 61, [181, 185], [200, 206]],
    },
    '87.DXR': {'folder': 'Internal', 'opaque': [[15, 19], 208]},
    '88.DXR': {
        'folder': 'Internal',
        'opaque': [32, [33, 38], [40, 46], 92, 93, 96, 97, 100, 101],
    },
    '90.DXR': {'folder': 'Internal', 'opaque': [1, 18, 19]},
    '91.DXR': {'folder': 'Internal', 'opaque': [1]},
    '92.DXR': {
        'folder': 'Internal',
        'opaque': [1],
        'range_no': {
            'can': 7,
            'background': 203,
            'neighbor': [12, 23],
            'dog': [36, 40],
            'audio1': [177, 178],
            'audio2': [195, 201],
            'dogAnimChart': 33,
        },
        'range_sv': {
            'can': 11,
            'background': 1,
            'neighbor': [16, 27],
            'dog': [40, 44],
            'audio1': [181, 182],
            'audio2': [199, 205],
            'dogAnimChart': 37,
        },
    },
    '94.DXR': {'folder': 'Internal', 'opaque': [200]},
    'CDDATA.CXT': {'folder': 'Standalone', 'opaque': [[629, 658]]},
    'PLUGIN.CST': {'folder': 'Standalone', 'opaque': [18]},
    '89.DXR': {  # Viola
        'file': '89.DXR',
        'folder': 'Internal',
        'range_sv': {
            'background': 1,
            'animation': [18, 20],
            'audio': [177, 177, 200, 202]
        },
        'opaque': [1],
        'identical': [[1, 1], [18, 20], [177, 177], [200, 202]],
    },
}


def resolve_list(data_list):
    if type(data_list) == int:
        return [data_list]
    elif type(data_list) == list:
        values = []
        """if type(data_list[0]) == int:
            return data_list"""

        for range_list in data_list:
            if type(range_list) == int:
                values.append(range_list)
            else:
                values += range(range_list[0], range_list[1] + 1)

        return values
