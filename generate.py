# -*- coding: utf-8 -*-
import music21
from decimal import Decimal
from decimal import getcontext
import decimal
from hyper import *
import random
import sys

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


def get_number_candidates(position):
    select_nums = PI[position: position+8]
    return select_nums


class DataGen(object):
    def __init__(self, numbers, **args):
        self.numbers = numbers

    def generate_notes(self, numbers, **kwargs):

        notes_list = []

        for num in numbers:
            p = MAPPING[num]
            if len(p) != 1:
                nt = music21.note.Rest()
            else:
                nt = music21.note.Note(MAPPING[p])

            nt.duration.quarterLength = 0.5
            notes_list.append(nt)

        return notes_list

    def get_chords(self, notes, **kwargs):
        return


if __name__ == '__main__':

    gen_midi = music21.stream.Score()
    # rand_pos = random.randint(8, MAX_INT)  # 溢出

    mode = 'major'
    bpm = ''
    chord_progress = ''

    rand_pos = random.randint(0, 10e3)  # 太久了运行
    print(rand_pos)
    select_nums = get_number_candidates(rand_pos)
    print(select_nums)




# print(get_pitch_candidates(1000))
