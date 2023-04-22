import os
import argparse
import random
import string
import numpy as np
from pedalboard import Pedalboard, Chorus, Distortion
from pedalboard.io import AudioFile

def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_output_filename(input_filename, random_suffix):
    return os.path.splitext(input_filename)[0] + "_gain_chorus_" + random_suffix + os.path.splitext(input_filename)[1]

def apply_gain_and_chorus(input_audio_file, input_ann_file, output_directory, gain, chorus_depth, chorus_rate):
    random_suffix = random_word(5)
    os.makedirs(output_directory, exist_ok=True)

    # Generate output audio file name and path
    output_audio_filename = generate_output_filename(os.path.basename(input_audio_file), random_suffix)
    output_audio_file_path = os.path.join(output_directory, output_audio_filename)

    with AudioFile(input_audio_file) as input_file:
        audio = input_file.read(input_file.frames)
        samplerate = input_file.samplerate

    gain_effect = Distortion(drive_db=gain)
    chorus_effect = Chorus(depth=chorus_depth, rate_hz=chorus_rate, centre_delay_ms=7.0, feedback=0.3, mix = 0.5)

    pedalboard = Pedalboard([gain_effect, chorus_effect])

    processed_audio = pedalboard(audio, samplerate)

    with AudioFile(output_audio_file_path, 'w', samplerate, audio.shape[0]) as output_file:
        output_file.write(processed_audio)

    # Copy the annotation file to the output directory with a modified name
    output_ann_filename = generate_output_filename(os.path.basename(input_ann_file), random_suffix)
    output_ann_file_path = os.path.join(output_directory, output_ann_filename)
    os.system(f'cp "{input_ann_file}" "{output_ann_file_path}"')
    return output_ann_file_path

def main():
    parser = argparse.ArgumentParser(description="Apply gain and chorus effects to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("gain", type=float, help="Gain for the gain effect")
    parser.add_argument("chorus_depth", type=float, help="Depth of the chorus effect (0 to 1)")
    parser.add_argument("chorus_rate", type=float, help="Rate of the chorus effect (in Hz)")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    apply_gain_and_chorus(args.input_audio_file, args.input_ann_file, args.output_directory, args.gain, args.chorus_depth, args.chorus_rate)

if __name__ == "__main__":
    main()
