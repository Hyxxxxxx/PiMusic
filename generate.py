# -*- coding: utf-8 -*-

import music21
from decimal import Decimal
from decimal import getcontext
import decimal
import numpy as np
from hyper import *
import random
from collections import Counter
import sys
from utils.midi2audio import *

MAX_INT = decimal.MAX_PREC


def useless(precision):
    """得到pi的精度，到指定的位数"""
    getcontext().prec = precision
    pi = sum(1 / Decimal(16) ** k *
             (Decimal(4) / (8 * k + 1) -
             Decimal(2) / (8 * k + 4) -
             Decimal(1) / (8 * k + 5) -
             Decimal(1) / (8 * k + 6)) for k in range(precision))
    str_pi = str(pi)
    select_nums = list(str_pi)[-8:]
    return select_nums


def get_number_candidates(position, nums=32):
    """ 获得 pi 数字组 """
    select_nums = PI[position: position+nums]
    select_nums = np.array(select_nums).reshape(-1, 8)

    return select_nums


def generate_notes(numbers, tempo):
    """ 生成旋律轨 """

    melody_part = music21.stream.Part()
    tempo_set(melody_part, tempo)

    note_ls = []

    note_info_dict = {}

    m = 1
    for nums in numbers:
        measure = music21.stream.Measure()

        notes = []
        for num in nums:
            p = MAPPING[num]
            if p == 'rest':
                nt = music21.note.Rest()
            else:
                notes.append(p)
                if len(note_ls) == 0:
                    n_str = p

                else:
                    last_n = note_ls[-1]

                    last_midi = last_n.pitch.midi
                    last_n_octave = music21.note.Note(last_midi).octave

                    candidate_oc = [-1, 0, 1]
                    deltas = []
                    for i in range(len(candidate_oc)):
                        d = abs(music21.note.Note(p+str(last_n_octave+candidate_oc[i])).pitch.midi - last_n.pitch.midi)
                        deltas.append(d)

                    select_delta = deltas.index(min(deltas))
                    n_str = p+str(last_n_octave+candidate_oc[select_delta])  # 找最近的那个音

                nt = music21.note.Note(n_str)
                note_ls.append(nt)

            nt.duration.quarterLength = 0.5
            measure.append(nt)

        note_info_dict['measure'+str(m)] = notes
        melody_part.append(measure)
        m += 1

    # melody_part.show()
    print(note_info_dict)
    return melody_part, note_info_dict


def generate_chords(chord_progress, note_info_dict, tempo):
    # note_info_dict 是每个小节的音符组成

    rand_chord = chord_progress[random.randint(0, len(chord_progress)-1)]
    print("Your chord progress: ", rand_chord)

    chord_part = music21.stream.Part()
    tempo_set(chord_part, tempo)

    chord_symbols = []
    nt_dict_keys = list(note_info_dict.keys())
    match_cnts = 0
    for i in range(len(note_info_dict)):

        chord_root = number2chord(int(str(rand_chord)[i]))

        if str(rand_chord)[i] not in MINOR_SCALE:

            prob = random.random()

            if prob < 0.5:
                if chord_root == 'G':
                    chord_root += '7'

                else:
                    chord_root += 'maj7'

            chord_component = music21.harmony.ChordSymbol(chord_root).pitches
            chord_symbols.append(music21.harmony.ChordSymbol(chord_root))

        else:
            # print(str(rand_chord)[i])
            chord_root += 'm'
            prob = random.random()

            if prob < 0.5:
                chord_root += '7'
            chord_component = music21.harmony.ChordSymbol(chord_root).pitches
            chord_symbols.append(music21.harmony.ChordSymbol(chord_root))

        chord = music21.chord.Chord(chord_component)
        chord.duration.quarterLength = 4.0
        chord_part.append(chord)

        chord_component = [c.name for c in chord_component]

        nts = note_info_dict[nt_dict_keys[i]]
        candidate_c = list(set([str(chord)[i] for chord in chord_progress]))

        candidate_tonic = []
        for ci in range(len(candidate_c)):
            tonic = number2chord(int(candidate_c[ci]))
            candidate_tonic.append(tonic)

        startNote = nts[0]
        endNote = nts[-1]
        collection_nts = Counter(nts)
        mostNote = collection_nts.most_common(1)[0][0]

        select_nts = [startNote, endNote, mostNote]

        # select_nts = list(set([startNote, endNote, mostNote]))
        print('\nchord component:', chord_component)
        print('stats notes: ', select_nts)

        cnt = compare2list(select_nts, chord_component)
        match_cnts += cnt

    match_ratio = match_cnts / 12
    print(match_cnts, match_ratio)

    return chord_part, match_cnts, match_ratio


def compare2list(list1, list2):
    """ 判断list1的字符是不是在list2中 """
    # flag = False
    cnt = 0
    for i in range(len(list1)):
        if list1[i] in list2:
            cnt += 1

    return cnt


def number2chord(n, key='C'):  # input 2, 'C' output D
    # minorScale = ['2', '3', '6', '7']  # 7是dim？
    sc1 = music21.scale.MajorScale(key)
    sc2 = [str(p) for p in sc1.getPitches(key + '3', key + '4')]
    tonic = sc2[n - 1][0]
    return tonic


def tempo_set(m, t):
    # input stream.score, 90 output score with new bpm
    tep = music21.tempo.MetronomeMark(number=t)
    m.insert(0.0, tep)
    return m


def concat_result(melody_part, chord_part, audioName='', composer=""):

    result = music21.stream.Score()
    result.insert(0, music21.metadata.Metadata())
    result.metadata.title = audioName
    result.metadata.composer = composer

    result.append(melody_part)
    result.append(chord_part)

    # print('----', MELODY_RES_ROOT)
    # wav_file = WAV_ROOT + audioName + '.wav'
    # mp3_file = MP3_ROOT + audioName + '.mp3'

    import time
    now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    midi_name = composer + '_' + audioName + now
    midi_file = MELODY_RES_ROOT + midi_name + '.mid'

    if midi_file in os.listdir(MELODY_RES_ROOT):
        midi_name += 'x'
        midi_file = MELODY_RES_ROOT + midi_name + '.mid'

    result.write('midi', fp=midi_file)
    from music21.converter.subConverters import ConverterMusicXML
    conv_musicxml = ConverterMusicXML()
    conv_musicxml.write(result, 'musicxml', fp=PNG_ROOT + midi_name + ".xml", subformats=['png'])
    png_file_path = PNG_ROOT + midi_name + "-1.png"

    wav_file = midi_to_wav(midi_name, MELODY_RES_ROOT, WAV_ROOT)
    mp3_file_path = wav_to_mp3(midi_name, WAV_ROOT, MP3_ROOT)

    # 返回mp3/png文件路径，及存储的曲名
    return mp3_file_path, png_file_path, midi_name


def generate_result(bpm, feelingChosen, title='', composer=''):

    rand_pos = random.randint(0, 10e3 - nums)
    print('Start your Pi from %s \n' % rand_pos)
    select_nums = get_number_candidates(rand_pos)
    melody_part, note_info_dict = generate_notes(numbers=select_nums, tempo=bpm)
    print(select_nums)

    chord_part, match_cnts, match_ratio = \
        generate_chords(chord_progress=EMOTION_DICT[feelingChosen],
                        note_info_dict=note_info_dict,
                        tempo=bpm)
    mp3_file_path, png_file_path, midi_name = concat_result(melody_part, chord_part,
                                                            audioName=title, composer=composer)
    return mp3_file_path, png_file_path, midi_name


if __name__ == '__main__':

    # rand_pos = random.randint(8, MAX_INT)  # 溢出

    mode = 'major'  # 调式没搞

    # 可选项
    bpm = 60
    feelingChosen = ''
    nums = 32

    generate_result(bpm=bpm, feelingChosen='SB',
                    title="gtmd", composer="vv")

    # m = music21.harmony.ChordSymbol('C7').pitches
    # m2 = music21.harmony.ChordSymbol('G7').pitches
    # m3 = music21.harmony.ChordSymbol('F7').pitches
    # m4 = music21.harmony.ChordSymbol('Em7').pitches

# print(get_pitch_candidates(1000))
