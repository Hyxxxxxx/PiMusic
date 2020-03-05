# -*- coding: utf-8 -*-

# Pitch mapping
MAPPING = {'0': 'rest', '1': 'C4', '2': 'D4', '3': 'E4',
           '4': 'F4', '5': 'G4', '6': 'A4', '7': 'B4',
           '8': 'C5', '9': 'D5'}

KEY_CANDIDATE = {'common': ['C', 'G', 'F'],
                 'less_common': ['bB', 'D']
                 }  # 大调

BPM = {'': 60, '超上头': 100}

MODE = {'': 'minor', '': 'minor', '': 'minor',
        '': 'major', '': 'major', '': 'major'}


with open('pi.txt', 'r') as pi_txt:
    lines = pi_txt.readlines()
    PI = list(lines[0])
    pi_txt.close()

    # for l in lines:
