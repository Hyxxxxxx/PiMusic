# -*- coding: utf-8 -*-
import os
import pandas as pd

CURR_ROOT = os.getcwd()
print("CURR: ", CURR_ROOT)
PARENT_ROOT = os.path.dirname(CURR_ROOT)
print("PARENT", PARENT_ROOT)
RESULT_ROOT = CURR_ROOT + "/result/"
MELODY_RES_ROOT = RESULT_ROOT + "midi/"
# print(MELODY_RES_ROOT)
WAV_ROOT = RESULT_ROOT + "wav/"
MP3_ROOT = RESULT_ROOT + "mp3/"
PNG_ROOT = RESULT_ROOT + "png/"


# Pitch mapping
MAPPING = {'0': 'rest', '1': 'C', '2': 'D', '3': 'E',
           '4': 'F', '5': 'G', '6': 'A', '7': 'B',
           '8': 'C', '9': 'D'}

KEY_CANDIDATE = {'common': ['C', 'G', 'F'],
                 'less_common': ['bB', 'D']
                 }  # 大调

BPM = {'': 60, '超上头': 100}

MODE = {'': 'minor', '': 'minor', '': 'minor',
        '': 'major', '': 'major', '': 'major'}


with open('src/pi.txt', 'r') as pi_txt:
    lines = pi_txt.readlines()
    PI = list(lines[0])
    pi_txt.close()

# 按照情绪选择和声进行
CHORDS = {
    "超有元気": "B",
    "添点元気": "SB",
    "随意套娃": "N",
    "羡慕的眼泪": "SE",
    "梦幻忧伤": "SEST"
}

xml_file_path = 'src/VER1.xlsx'
startNum = pd.read_excel(xml_file_path, sheet_name='start')  #
tempoNum = pd.read_excel(xml_file_path, sheet_name='tempo')

EMOTION = ['B', 'SB', 'N', 'SE', 'SEST']

EMOTION_DICT = {}

for i in range(len(EMOTION)):
    startNumbers = list(startNum.loc[:, EMOTION[i]].dropna())  # 非空的
    EMOTION_DICT[EMOTION[i]] = startNumbers

# print(EMOTION_DICT)

MINOR_SCALE = ['2', '3', '6', '7']  # 7是dim？

