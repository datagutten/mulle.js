#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
from subprocess import call

from PyTexturePacker import ImageRect
from PyTexturePacker import Packer
from PyTexturePacker import Utils as PyTexturePackerUtils

from audiosprite import AudioSprite
from build_scripts.MulleResource import MulleResource
from build_scripts.convert_image import convert_image
from build_scripts.data import director_data
from build_scripts.parse_animation_chart import parse_animation_chart

optimizeImages = int(sys.argv[1])

MulleResources = []

resMenu = MulleResource('menu')
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': 2})
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': '115-123'})  # face
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': '125-138'})  # mulle
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': '156-163'})  # buffa
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': '169-170'})  # toilet
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': '287-292'})  # intro audio
resMenu.addFile({'dir': '10.DXR', 'lib': 'Internal', 'num': '300-307'})  # menu audio
MulleResources.append(resMenu)

resParts = MulleResource('carparts')
resParts.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '239-312'})
resParts.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '316-496'})
resParts.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '838-917'})
resParts.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '966-1018'})
resParts.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '1213-1390'})  # audio
MulleResources.append(resParts)

resMap = MulleResource('map')
resMap.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '629-658'})
resMap.opaque = True
MulleResources.append(resMap)

resDriving = MulleResource('driving')
# resDriving.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '34-238'})  # PartsDB
resDriving.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '497-514'})  # images
resDriving.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '565-598'})  # audio
resDriving.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '599-624'})  # images
resDriving.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': 625})  # audio
resDriving.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '626-628'})  # images

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': 21})  # ui
resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': 25})  # dashboard

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '27-42'})  # fuel meter

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': 46})  # speed meter

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': 53})  # menu

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '69-75'})  # medals

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '77-157'})  # car

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '161-192'})  # pointer

resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '233-249'})  # voices
# resDriving.addFile({ 'dir': '05.DXR', 'lib': 'Internal', 'num': '265-266' }) # skid
resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '269-275'})  # horns
resDriving.addFile({'dir': '05.DXR', 'lib': 'Internal', 'num': '294-369'})  # engine

MulleResources.append(resDriving)

resGarage = MulleResource('garage')
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': 33})  # back
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '34-40'})  # doors

resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '81-93'})  # figge
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '107-108'})  # figge truck

resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '101-105'})  # phone and hover
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '181-183'})  # ui sounds
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '208-223'})  # voices
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '226-258'})  # voices
resGarage.addFile({'dir': '03.DXR', 'lib': 'Internal', 'num': '262-264'})  # voice remarks
resGarage.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': 23})  # Phone audio roaddog
resGarage.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '26-28'})  # Phone audio doris/mia/lasse
MulleResources.append(resGarage)

resYard = MulleResource('yard')
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': '13-14'})
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': 16})
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': 27})
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': 30})
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': 37})  # Background
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': '40-44'})
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': 261})  # No mail
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': '272-277'})  # Package and garage full
resYard.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': '279-280'})  # Mail/figge
resYard.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '19-22'})  # Letters
resYard.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '24-25'})  # Letter audio carshow/sturestortand
resYard.addFile({'dir': 'CDDATA.CXT', 'lib': 'Standalone', 'num': '29-30'})  # Letter audio pia/race

MulleResources.append(resYard)

resAlbum = MulleResource('album')
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': '21-27'})  # Medals
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': '38-40'})  # UI sounds
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': '49-84'})  # Page numbers
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': 93})  # Page
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': '97-101'})  # Page
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': '137-150'})  # Sounds
resAlbum.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': '153-164'})  # UI
MulleResources.append(resAlbum)

resBrowser = MulleResource('fileBrowser')
resBrowser.addFile({'dir': '13.DXR', 'lib': 'Internal', 'num': 17})  # Audio
resBrowser.addFile({'dir': '13.DXR', 'lib': 'Internal', 'num': 29})  # Scroll
resBrowser.addFile({'dir': '13.DXR', 'lib': 'Internal', 'num': 32})  # File browser
MulleResources.append(resBrowser)

resDiploma = MulleResource('diploma')
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': 15})
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': '17-18'})
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': '21-27'})
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': 31})
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': '39-40'})
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': '66-71'})
resDiploma.addFile({'dir': '08.DXR', 'lib': 'Internal', 'num': '81-86'})  # Strings
MulleResources.append(resDiploma)

resCutscenes = MulleResource('cutscenes')
resCutscenes.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '66-76'})
resCutscenes.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': 81})
resCutscenes.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '83-86'})
MulleResources.append(resCutscenes)

resUI = MulleResource('ui')
resUI.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': 97})
resUI.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '109-117'})
MulleResources.append(resUI)

resCharacters = MulleResource('characters')
resCharacters.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '214-227'})  # buffa
resCharacters.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '245-263'})  # car
resCharacters.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '271-302'})  # car
MulleResources.append(resCharacters)

resShared = MulleResource('shared')
resShared.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '416-421'})  # misc audio
resShared.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '433-461'})  # misc audio
resShared.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '469-474'})  # misc audio
resShared.addFile({'dir': '00.CXT', 'lib': 'Standalone', 'num': '485-493'})  # misc audio
resShared.addFile({'dir': '04.DXR', 'lib': 'Internal', 'num': '48-49'})  # mailbox audio
MulleResources.append(resShared)

resJunk = MulleResource('junk')
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': 66})  # bg
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '68-72'})  # bg
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '85-96'})  # doors
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '162-185'})  # arrows
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '122-137'})  # sounds
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '209-210'})  # body
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '226-243'})  # head right
resJunk.addFile({'dir': '02.DXR', 'lib': 'Internal', 'num': '246-263'})  # head left
MulleResources.append(resJunk)

resRoadDog = MulleResource('roaddog')
resRoadDog.addFile({'dir': '85.DXR', 'lib': 'Internal', 'num': 25})  # images
resRoadDog.addFile({'dir': '85.DXR', 'lib': 'Internal', 'num': '190'})  # audio
resRoadDog.addFile({'dir': '85.DXR', 'lib': 'Internal', 'num': '200-201'})  # audio
resRoadDog.addFile({'dir': '85.DXR', 'lib': 'Internal', 'num': '26-34'})  # salka right
MulleResources.append(resRoadDog)

if os.path.exists(os.path.join('cst_out_new', '66.DXR')):
    resPlugin = MulleResource('plugin')
    # [25,27, , [38, 42], 45, [51, 56], [57,59], [68,78], [81, 94], [97, 115]]
    resPlugin.addFile({'dir': '66.DXR', 'lib': 'Internal', 'num': 25})  # Background
    resPlugin.addFile({'dir': '66.DXR', 'lib': 'Internal', 'num': [33, 37]})  # Junk
    resPlugin.addFile({'dir': '66.DXR', 'lib': 'Internal', 'num': [38, 42]})  # Sounds
    resPlugin.addFile({'dir': '66.DXR', 'lib': 'Internal', 'num': [51, 56]})  #
    resPlugin.addFile({'dir': '66.DXR', 'lib': 'Internal', 'num': [57, 59]})  # Crane
    resPlugin.addFile({'dir': '66.DXR', 'lib': 'Internal', 'num': [69, 78]})  # Figge
    resPlugin.addFile({'dir': '06.DXR', 'lib': 'Internal', 'num': 153})  # Close button
    resPlugin.addFile({'dir': 'PLUGIN.CST', 'lib': 'Standalone', 'num': [21, 47]})  # Parts
    MulleResources.append(resPlugin)

resMudCar = MulleResource('mudcar')
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': 1})  # background
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': '17-19'})  # moose
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': '25-39'})  # driver and rope
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': '41-44'})  # stuck car
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': '49-57'})  # buffa
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': 83})
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': '173-174'})
resMudCar.addFile({'dir': '82.DXR', 'lib': 'Internal', 'num': '200-202'})
MulleResources.append(resMudCar)

resRoadTree = MulleResource('roadtree')
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '1-3'})  # background and car
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '13-15'})  # driver animation
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '21-28'})  # tree
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '33-38'})  # boffa
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '45-91'})  # mulle
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '93-97'})  # driver talk animation frames
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': 99})  # driver talk animation
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': 113})
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '181-183'})  # sounds
resRoadTree.addFile({'dir': '83.DXR', 'lib': 'Internal', 'num': '200-204'})  # sounds
MulleResources.append(resRoadTree)

resRoadThing = MulleResource('roadthing')
resRoadThing.addFile({'dir': '84.DXR', 'lib': 'Internal', 'num': 25})  # images
resRoadThing.addFile({'dir': '84.DXR', 'lib': 'Internal', 'num': 201})  # audio
resRoadThing.addFile({'dir': '00.CXT', 'lib': 'Internal', 'num': 446})  # audio ding
MulleResources.append(resRoadThing)

resLuddeLabb = MulleResource('luddelabb')
resLuddeLabb.addFile({'dir': '91.DXR', 'lib': 'Internal', 'num': 1})
resLuddeLabb.addFile({'dir': '91.DXR', 'lib': 'Internal', 'num': 174})
resLuddeLabb.addFile({'dir': '91.DXR', 'lib': 'Internal', 'num': '200-202'})
MulleResources.append(resLuddeLabb)

resFiggeFerrum = MulleResource('figgeferrum')
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': 1})  # Background
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': 11})  # Gas can
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': '16-27'})
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': 37})  # DogAnimChart
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': '40-44'})  # Salka frames
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': '181-182'})  # sound
resFiggeFerrum.addFile({'dir': '92.DXR', 'lib': 'Internal', 'num': '199-205'})  # sound
MulleResources.append(resFiggeFerrum)

resStureStortand = MulleResource('sturestortand')
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '16-25'})  # tube
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '32-46'})  # sture and bg
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '92-93'})  # kids 1
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '96-97'})  # kids 2
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '100-101'})  # kids 3
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '92-93'})  # kids 1
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': 181})  # bg loop
resStureStortand.addFile({'dir': '88.DXR', 'lib': 'Internal', 'num': '199-204'})  # audio
MulleResources.append(resStureStortand)

resSaftfabrik = MulleResource('saftfabrik')
resSaftfabrik.addFile({'dir': '87.DXR', 'lib': 'Internal', 'num': '15-18'})  # gaston
resSaftfabrik.addFile({'dir': '87.DXR', 'lib': 'Internal', 'num': '26-29'})  # splash
resSaftfabrik.addFile({'dir': '87.DXR', 'lib': 'Internal', 'num': 185})  # bg loop
resSaftfabrik.addFile({'dir': '87.DXR', 'lib': 'Internal', 'num': '200-206'})  # audio
resSaftfabrik.addFile({'dir': '87.DXR', 'lib': 'Internal', 'num': 208})  # bg image
MulleResources.append(resSaftfabrik)

resCarShow = MulleResource('carshow')
resCarShow.addFile({'dir': '94.DXR', 'lib': 'Internal', 'num': '17-21'})  # numbers
resCarShow.addFile({'dir': '94.DXR', 'lib': 'Internal', 'num': '31-47'})  # judge
resCarShow.addFile({'dir': '94.DXR', 'lib': 'Internal', 'num': 185})  # bg noise
resCarShow.addFile({'dir': '94.DXR', 'lib': 'Internal', 'num': 200})  # bg image
resCarShow.addFile({'dir': '94.DXR', 'lib': 'Internal', 'num': '201-209'})  # speech
MulleResources.append(resCarShow)

resSolhem = MulleResource('solhem')
resSolhem.addFile({'dir': '86.DXR', 'lib': 'Internal', 'num': 1})
resSolhem.addFile({'dir': '86.DXR', 'lib': 'Internal', 'num': 3})
resSolhem.addFile({'dir': '86.DXR', 'lib': 'Internal', 'num': 21})
resSolhem.addFile({'dir': '86.DXR', 'lib': 'Internal', 'num': '30-74'})
resSolhem.addFile({'dir': '86.DXR', 'lib': 'Internal', 'num': '181-185'})
resSolhem.addFile({'dir': '86.DXR', 'lib': 'Internal', 'num': '200-206'})
MulleResources.append(resSolhem)

resDoris = MulleResource('dorisdigital')
resDoris.addFile({'dir': '90.DXR', 'lib': 'Internal', 'num': 1})  # Outside
resDoris.addFile({'dir': '90.DXR', 'lib': 'Internal', 'num': '18-19'})  # Window
resDoris.addFile({'dir': '90.DXR', 'lib': 'Internal', 'num': 185})  # Game sounds
resDoris.addFile({'dir': '90.DXR', 'lib': 'Internal', 'num': '200-202'})  # Speech
MulleResources.append(resDoris)

assetOutPath = "./dist/assets"
if not os.path.exists(assetOutPath):
    os.makedirs(assetOutPath)
assetWebPath = "assets"
resourcePath = 'cst_out_new'
if not os.path.exists(resourcePath):
    raise FileNotFoundError(resourcePath)
meta = {}

assetIndex = {}

for res in MulleResources:

    resName = res.name

    assetIndex[resName] = {'files': []}

    print("")
    print("- " + resName)

    atlasData = {}
    soundSprite = {}
    textString = {}
    animations = {}

    imageRects = []

    packFiles = {}
    packFiles[resName] = []

    for f in res.files:

        dirPath = resourcePath + '/' + f['dir']

        j = None

        if f['dir'] in meta:
            j = meta[f['dir']]
        else:
            # j = require( dirPath + '/metadata.json');

            with open(dirPath + '/metadata.json') as data_file:
                j = json.load(data_file)

            meta[f['dir']] = j

        lib = j['libraries'][0]

        if str(f['num']) in lib['members']:
            mem = lib['members'][str(f['num'])]
        else:
            print("[" + res.name + "] Invalid file " + f['dir'] + " " + str(lib['name']) + " " + str(f['num']))
            continue

        libPath = dirPath + '/' + lib['name']

        fileBasePath = libPath + '/' + str(f['num'])

        if mem['castType'] == 1:
            movie = f['dir']
            opaque = []
            if movie in director_data.data:
                if 'opaque' in director_data.data[movie]:
                    opaque += director_data.resolve_list(director_data.data[movie]['opaque'])
                if 'opaque_sv' in director_data.data[movie]:
                    opaque += director_data.resolve_list(director_data.data[movie]['opaque_sv'])
            else:
                print('No opaque data for %s' % movie)

            if not os.path.exists(fileBasePath + '.bmp'):
                print('Missing file %s' % fileBasePath + '.bmp')
                continue

            if f['num'] in opaque:
                convert_image(fileBasePath + '.bmp', False)
            else:
                convert_image(fileBasePath + '.bmp')

            filePath = fileBasePath + ".png"

            intName = str(len(atlasData) + 1)

            p = {}

            p['path'] = filePath;

            p['width'] = mem['imageWidth'];
            p['height'] = mem['imageHeight'];

            p['data'] = {}

            # p['data']['name'] = (atlasData.length + 1).toString();

            p['data']['pivotX'] = mem['imageRegX']
            p['data']['pivotY'] = mem['imageRegY']

            p['data']['dirFile'] = f['dir']
            p['data']['dirName'] = mem['name']
            p['data']['dirNum'] = f['num']

            # atlasData.push( p );
            atlasData[intName] = p

            assetIndex[resName]['files'].append(
                {'type': 'image', 'dirFile': f['dir'], 'dirName': mem['name'], 'dirNum': f['num']})

            image_rect = ImageRect.ImageRect(filePath)

            original = None

            for v in imageRects:
                # print("compare " + str( p['data']['dirFile'] ) + " " + str( p['data']['dirNum'] ) + " == " + str( v.dirFile ) + " " + str( v.dirNum ) )
                # diff = ImageChops.difference(image_rect.image, v.image)
                # print("diff " + str(diff))
                if mem['imageHash'] == v.hash:
                    original = v
                    break

            if original is not None:
                # print("found duplicate")

                dupe = {}
                dupe['pivot'] = {'x': p['data']['pivotX'], 'y': p['data']['pivotY']}
                dupe['baseName'] = intName
                dupe['dirFile'] = p['data']['dirFile']
                dupe['dirName'] = p['data']['dirName']
                dupe['dirNum'] = p['data']['dirNum']

                original.dupes.append(dupe)
            else:
                image_rect.pivot = {'x': p['data']['pivotX'], 'y': p['data']['pivotY']}
                image_rect.baseName = intName
                image_rect.dirFile = p['data']['dirFile']
                image_rect.dirName = p['data']['dirName']
                image_rect.dirNum = p['data']['dirNum']
                image_rect.hash = mem['imageHash']
                image_rect.dupes = []

                imageRects.append(image_rect)

        # print("image " + f['dir'] + " " + str(lib['name']) + " " + str(f['num']))
        else:
            p = {'data': {}}
            p['data']['dirName'] = mem['name']
            p['data']['dirFile'] = f['dir']
            p['data']['dirNum'] = f['num']

            if mem['castType'] == 6:
                filePath = fileBasePath + ".wav"
                p['path'] = filePath

                if 'soundLooped' in mem:
                    p['loop'] = mem['soundLooped']
                else:
                    p['loop'] = False

                if 'soundCuePoints' in mem and len(mem['soundCuePoints']) > 0:
                    p['data']['cue'] = mem['soundCuePoints']

                soundSprite[str(len(soundSprite) + 1)] = p

                assetIndex[resName]['files'].append(
                    {'type': 'sound', 'dirFile': f['dir'], 'dirName': mem['name'], 'dirNum': f['num']})

            # print("audio " + f['dir'] + " " + str(lib['name']) + " " + str(f['num']))

            if mem['castType'] == 12 or mem['castType'] == 3:
                if f['dir'] not in textString:
                    textString[f['dir']] = {}

                filePath = fileBasePath + ".txt"
                p['path'] = filePath
                fp = open(filePath, 'rb')
                string = fp.read()
                string = string.decode('iso8859-1')
                if mem['castType'] == 12:
                    textString[f['dir']][f['num']] = string
                elif mem['castType'] == 3:
                    if f['dir'] not in animations:
                        animations[f['dir']] = {}
                    try:
                        animations[f['dir']][f['num']] = parse_animation_chart(string)
                    except RuntimeError as e:
                        print(str(e))
                        textString[f['dir']][f['num']] = string

    if len(textString) > 0:
        file = '%s/%s-strings.json' % (assetOutPath, resName)
        fp = open(file, 'w')
        json.dump(textString, fp)

    if len(animations) > 0:
        file = '%s/%s-animations.json' % (assetOutPath, resName)
        fp = open(file, 'w')
        json.dump(animations, fp)

    print("Images: " + str(len(imageRects)))
    print("Sounds: " + str(len(soundSprite)))
    print("Strings: " + str(len(textString)))
    print("Animations: " + str(len(animations)))

    if len(imageRects) > 0:
        if res.opaque:
            packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffffff, trim_mode=1,
                                   enable_rotated=False)
        else:
            packer = Packer.create(max_width=2048, max_height=2048, bg_color=0x00ffffff, trim_mode=1,
                                   enable_rotated=False)

        atlas_list = packer._pack(imageRects)

        for i, atlas in enumerate(atlas_list):
            print("Pack image " + str(i))

            fSprites = {}
            fSprites['frames'] = {}

            packed_image = atlas.dump_image(packer.bg_color)

            atlasName = resName + '-sprites-' + str(i)

            PyTexturePackerUtils.save_image(packed_image, assetOutPath + "/" + atlasName + '.png')

            if optimizeImages > 0:
                call(['optipng', '-o', str(optimizeImages), os.path.join(assetOutPath, atlasName + '.png')])

            # make json
            for image_rect in atlas.image_rect_list:
                width, height = (image_rect.width, image_rect.height) if not image_rect.rotated \
                    else (image_rect.height, image_rect.width)

                center_offset = (0, 0)
                if image_rect.trimmed:
                    center_offset = (image_rect.source_box[0] + width / 2. - image_rect.source_size[0] / 2.,
                                     - (image_rect.source_box[1] + height / 2. - image_rect.source_size[1] / 2.))

                m = {}
                m['frame'] = {"x": image_rect.x, "y": image_rect.y, "w": width, "h": height}
                m['regpoint'] = image_rect.pivot
                m['dirFile'] = image_rect.dirFile
                m['dirName'] = image_rect.dirName
                m['dirNum'] = image_rect.dirNum

                fSprites['frames'][image_rect.baseName] = m

                if len(image_rect.dupes) > 0:
                    for dupe in image_rect.dupes:
                        n = {}
                        n['frame'] = {"x": image_rect.x, "y": image_rect.y, "w": width, "h": height}
                        n['regpoint'] = dupe['pivot']
                        n['dirFile'] = dupe['dirFile']
                        n['dirName'] = dupe['dirName']
                        n['dirNum'] = dupe['dirNum']

                        fSprites['frames'][dupe['baseName']] = n

                    # print("dupe handled: " + dupe['dirFile'] + " - " + str(dupe['dirNum']) )

            fSprites['meta'] = {
                "size": {"w": packed_image.size[0], "h": packed_image.size[1]},
                "image": assetWebPath + '/' + atlasName + '.png',
                "scale": "1",
            }

            fSpritesOut = open(assetOutPath + "/" + atlasName + ".json", "w")
            fSpritesOut.write(json.dumps(fSprites))
            fSpritesOut.close()

            packFiles[resName].append({
                "type": "atlasJSONHash",
                "key": atlasName,
                "textureURL": assetWebPath + '/' + atlasName + '.png',
                "atlasURL": assetWebPath + '/' + atlasName + '.json',
                "atlasData": None
            })

    if len(soundSprite) > 0:
        sprite = AudioSprite(resName)

        for s in soundSprite:
            sprite.addAudio(soundSprite[s]['path'], isLooped=soundSprite[s]['loop'], extraData=soundSprite[s]['data'])

        outSprite = sprite.save(assetOutPath, resName + '-audio', formats=['ogg'], bitrate='32k',
                                parameters=['-ar', '22050'])

        packFiles[resName].append({
            "type": "audiosprite",
            "key": resName + "-audio",
            "urls": assetWebPath + '/' + resName + '-audio.ogg',
            "jsonURL": assetWebPath + '/' + resName + '-audio.json',
            "jsonData": None
        })

    fPackOut = open(assetOutPath + "/" + resName + ".json", "w")
    fPackOut.write(json.dumps(packFiles))
    fPackOut.close()

fIndexOut = open(assetOutPath + "/index.json", "w")
fIndexOut.write(json.dumps(assetIndex))
fIndexOut.close()
