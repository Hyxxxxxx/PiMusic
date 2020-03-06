import glob
import platform
import os
# print(platform.system())


# file to file
def midi_to_wav(file_name, midi_root, wav_root):
    # sf_path = "/Users/viviane/Documents/一些奇怪的项目代码/MagicMusic/MelodyUpdate/MuseScore_General.sf3"

    midi_file = midi_root + file_name + '.mid'
    wav_file = wav_root + file_name + '.wav'
    print(midi_file, wav_file)

    # cmd = f'fluidsynth -a jack  -o synth.gain=.8    ' \
    #     f'-CO -RI -T wav  -F {wav_file} {sf_path} {midi_file}'
    cmd = f'timidity --output-24bit --output-mono -A120 {midi_file} -Ow -o {wav_file}'

    os.system(cmd)
    return wav_file


def wav_to_mp3(file_name, wav_root, mp3_root):
    wav_file = wav_root + file_name + '.wav'
    mp3_file = mp3_root + file_name + '.mp3'

    cmd = f'ffmpeg -i {wav_file} -b:a 64k -acodec mp3 -ar 44100 -ac 2 {mp3_file}'
    os.system(cmd)
    return mp3_file
