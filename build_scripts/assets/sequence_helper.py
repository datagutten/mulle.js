import json
import re
from json import JSONDecodeError
from typing import List


def convert_sequence(data: str) -> dict:
    data = data.replace('[', '{').replace(']', '}')
    data = re.sub(r'#(\w+):', r'"\1":', data)
    data = re.sub(r'(#\w+)', r'"\1"', data)
    data = re.sub(r'(\w+\(.+?\))[,\s]*', '', data)  # Remove parenthesis function calls
    data = data.replace('{}', '[]')  # Empty sequence
    data = re.sub(r'{([^:{}]+)}', r'[\1]', data)  # Fix non-nested lists
    while True:
        data, count = re.subn(r'{([^:]+)}', r'[\1]', data)
        if count == 0:
            break
    try:
        return json.loads(data)
    except JSONDecodeError as e:
        if e.msg == 'Extra data':
            return json.loads(data[:e.pos])
        if data[e.pos:e.pos + 3] == '}]]':
            fix = data[:e.pos] + ']]}' + data[e.pos + 3:]
            return json.loads(fix)
        else:
            raise e


def split_sequences(data) -> List[str]:
    sequences = []
    left = 0
    right = 0
    start = None
    depth = 0

    length = len(data)
    for pos, char in enumerate(data):
        if char == '[':
            depth += 1
            if start is None:
                start = pos
            left += 1
        if char == ']':
            depth -= 1
            right += 1

        if start is not None and pos > start and depth == 0:
            group = data[start:pos + 1]
            sequences.append(group)
            if pos + 1 < length and data[pos + 1] == '[':
                sequences += split_sequences(data[pos + 1:])
            return sequences
    raise RuntimeError('No valid sequence found')


def parse_animations(data: str):
    action_data = convert_sequence(data)
    animations = {}
    if not 'Actions' in action_data:
        raise RuntimeError("Invalid animation, Actions not found")
    for action, frames in action_data['Actions'].items():
        animations[action] = frames
        frames_resolved = []
        for frame in frames:
            if type(frame) is str and frame[0] == '#' and False:
                frames_resolved += animations[frame[1:]]  # TODO: Resolve cross references
            elif type(frame) is list:
                frames_resolved.append({
                    'function': frame[0][1:],
                    'args': frame[1:] if len(frame) > 2 else frame[1]
                })
            else:
                frames_resolved.append(frame)
            animations[action] = frames_resolved
    return animations


if __name__ == '__main__':
    samples = [
        '[#Actions:[#Still:[1], #Wait:[[#RndHold, 1,1,2],#Shrug,#Shrug,#Shrug,#Shrug,#Shrug,#Shrug,#Shrug,#Shrug,#Shrug, #Shrug,#talk], #Talk:[[#Sound,["00e017v0","00e018v0","00e019v0"]],49,50,50,49,49,49,50,50,[#RndHold,49,10,20]], #Shrug:[[#Sound,["00e032v0","00e033v0","00e034v0"]],41,41,42,42], #GetDown:[41,41,[#Sound,["00e031v0"]],42,42,42,42,43,43,44,44,45,45], #GetUp:[45,45,44,44,43,43,42,42,41,41], #Sleep:[[#RndHold,6,12,18],[#Sound, ["00e037v0","00e038v0"]],7,7,8,8,8,8,8,8,8,7,7], #WalkRightStart:[1,2,3,4,5,6,7,8], #WalkRight:[[#Sound,["00e014v0","00e015v0"]],9,10,11,12,13,14,15,16], #WalkRightStop:[17,18,19,20], #WalkLeftStart:[21,22,23,24,25,26,27,28], #WalkLeft:[[#Sound,["00e014v0","00e015v0"]],29,30,31,32,33,34,35,36], #WalkLeftStop:[37,38,39,40]], #Paths:[#Test:[point(0,0), point(0,0)]]]'
        "[#Actions:[#Still:[1], #Wait:[1, #Still], #Talk:[1,2,3,4,5,6,7,8],#TalkToMe:[9,10,11,12,13,14,15,16,17,18]], #Paths:[#Test:[point(100,100), point(200,200)]]]",
        "[#Actions:[#Still:[1], #Wait:[[#RndHold, 0, 10, 44], #Blink], #Talk:[2,3,[#RndFrame, [1,2,3,4]],4,5], #Blink:[6]], #Paths:[]]",
        '[#partId: 306, #master: 0, #MorphsTo: 0, #description: "20d003v0", #junkView: "20b306v1", #UseView: "20b306v2", #UseView2: "", #offset: [0, 0], #Properties: [#Weight: 5, #Speed: 5, #Fuelconsumption: 4, #Strength: 5, #Enginetype: 9], #Requires: [#a16, #a20], #Covers: [#a20, #a16], #new: 0]',
        '[#Actions:[#wift:[1,2,3,4,5,3,2,1]], #Paths:[]]',
        '[#Actions:[#Still:[1], #Wait:[[#RndHold,1,11,45],#Still], #Talk:[2,3,[#RndFrame,[2,3,4,5,6,7,8]],4,5], #Blink:[9,9]], #Paths:[]]',
        '[#Actions:[#Still:[1],#Svag:[1,1,1,1,1,2,2,3,3,4,4,5,5,5,5,5,5,4,4,3,3,2,2,4,4,5,5,5,5,5]], #Paths:[]]'
    ]

    for entry in samples:
        for sequence in split_sequences(entry):
            converted = convert_sequence(sequence)
