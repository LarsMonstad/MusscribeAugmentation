import os
import argparse
import random
import string
import numpy as np
from pedalboard import Pedalboard, Reverb, LowpassFilter, HighpassFilter
from pedalboard.io import AudioFile


def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


# Ranges 

#Reverb 0  off. low to high range: 30 - 100  
#Lowpass 20000 off. low to high range: 16300 - 17500
#Highpass 20 off. low to high range: 4000 - 7000

# Usage examples:
# Reverb:
# 1. No reverb: python reverbfilter.py input.flac input.ann output 0 20000 20
# 2. Low reverb: python reverbfilter.py input.flac input.ann output 30 20000 20
# 3. High reverb: python reverbfilter.py input.flac input.ann output 100 20000 20
#
# Lowpass:
# 1. No lowpass: python reverbfilter.py input.flac input.ann output 0 20000 20
# 2. Low lowpass: python reverbfilter.py input.flac input.ann output 0 16300 20
# 3. High lowpass: python reverbfilter.py input.flac input.ann output 0 17500 20
#
# Highpass:
# 1. No highpass: python reverbfilter.py input.flac input.ann output 0 20000 20
# 2. Low highpass: python reverbfilter.py input.flac input.ann output 0 20000 4000
# 3. High highpass: python reverbfilter.py input.flac input.ann output 0 20000 7000


def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_output_filename(input_filename, random_suffix):
    return os.path.splitext(input_filename)[0] + "_reverb_filters_" + random_suffix + os.path.splitext(input_filename)[1]


def apply_reverb_and_filters(input_audio_file, input_ann_file, output_directory, room_size, low_cutoff, high_cutoff):
    random_suffix = random_word(5)
    os.makedirs(output_directory, exist_ok=True)

    # Generate output audio file name and path
    output_audio_filename = generate_output_filename(os.path.basename(input_audio_file), random_suffix)
    output_audio_file_path = os.path.join(output_directory, output_audio_filename)

    with AudioFile(input_audio_file) as input_file:
        audio = input_file.read(input_file.frames)
        samplerate = input_file.samplerate

    reverb_effect = Reverb(room_size=room_size / 100.0, wet_level=room_size / 100.0)
    low_pass_filter = LowpassFilter(cutoff_frequency_hz=low_cutoff)
    high_pass_filter = HighpassFilter(cutoff_frequency_hz=high_cutoff)

    pedalboard = Pedalboard([reverb_effect, low_pass_filter, high_pass_filter])

    processed_audio = pedalboard(audio, samplerate)

    with AudioFile(output_audio_file_path, 'w', samplerate, audio.shape[0]) as output_file:
        output_file.write(processed_audio)


    # Copy the annotation file to the output directory with a modified name
    output_ann_filename = generate_output_filename(os.path.basename(input_ann_file), random_suffix)
    output_ann_file_path = os.path.join(output_directory, output_ann_filename)
    os.system(f'cp "{input_ann_file}" "{output_ann_file_path}"')


def main():
    parser = argparse.ArgumentParser(description="Apply reverb and filters to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("room_scale", type=float, help="Room scale and reverberance (0 to 100)")
    parser.add_argument("low_cutoff", type=int, default=20000, help="LowPassFilter cutoff frequency (20 to 20000)")
    parser.add_argument("high_cutoff", type=float, default=20, help="HighPassFilter cutoff frequency (20 to 20000)")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    apply_reverb_and_filters(args.input_audio_file, args.input_ann_file, args.output_directory, args.room_scale, args.low_cutoff, args.high_cutoff)


if __name__ == "__main__":
    main()
