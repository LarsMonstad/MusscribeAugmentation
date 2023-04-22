import os
import argparse
import random
import string
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment


# range 8 high 3 low  0 off

# Usage examples:
# Distortion
# 1. No Distortion python distortion.py input.flac input.ann outputfolder 0 
# 2. Low Distortion python distortion.py input.flac input.ann outputfolder 3 
# 3. High Distortion python distortion.py input.flac input.ann output 8 

def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_output_filename(input_filename, suffix):
    return os.path.splitext(input_filename)[0] + "_" + suffix + os.path.splitext(input_filename)[1]

def apply_distortion(input_audio_file, input_ann_file, output_directory, gain):
    random_suffix = random_word(5)
    os.makedirs(output_directory, exist_ok=True)

    # Generate output audio file name and path
    output_audio_filename = generate_output_filename(os.path.basename(input_audio_file), "distortion_" + random_suffix)
    output_audio_file_path = os.path.join(output_directory, output_audio_filename)

    samples, sample_rate = librosa.load(input_audio_file, sr=None, mono=False)
    channels = samples.shape[0]

    input_audio = AudioSegment.from_file(input_audio_file, format='flac', channels=channels, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)

    output_audio = input_audio.apply_gain(gain)

    output_audio.export(output_audio_file_path, format='flac')

    # Copy the annotation file to the output directory with a modified name
    output_ann_filename = generate_output_filename(os.path.basename(input_ann_file), "distortion_" + random_suffix)
    output_ann_file_path = os.path.join(output_directory, output_ann_filename)
    os.system(f'cp "{input_ann_file}" "{output_ann_file_path}"')

def main():
    parser = argparse.ArgumentParser(description="Apply distortion to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("gain", type=float, help="Gain for the distortion effect")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    apply_distortion(args.input_audio_file, args.input_ann_file, args.output_directory, args.gain)

if __name__ == "__main__":
    main()

