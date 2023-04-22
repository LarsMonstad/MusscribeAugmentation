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
# 3. High Distortion python distortion.py input.flac input.ann outputfolder 8 

def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def apply_distortion(audio_file, output_audio_file, gain):
    samples, sample_rate = librosa.load(audio_file, sr=None, mono=False)
    channels = samples.shape[0]

    input_audio = AudioSegment.from_file(audio_file, format='flac', channels=channels, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)
    
    output_audio = input_audio.apply_gain(gain)
    
    output_audio.export(output_audio_file, format='flac')

def main():
    parser = argparse.ArgumentParser(description="Apply distortion to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("gain", type=float, help="Gain for the distortion effect")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)
    input_filename = os.path.basename(args.input_audio_file)
    random_suffix = random_word(5)
    output_filename = os.path.splitext(input_filename)[0] + "_distortion_" + random_suffix + os.path.splitext(input_filename)[1]
    output_file_path = os.path.join(args.output_directory, output_filename)

    apply_distortion(args.input_audio_file, output_file_path, args.gain)

    # Copy the annotation file to the output directory without modifying it
    output_ann_filename = os.path.splitext(os.path.basename(args.input_ann_file))[0] + "_distortion_" + random_suffix + os.path.splitext(args.input_ann_file)[1]
    output_ann_file_path = os.path.join(args.output_directory, output_ann_filename)
    os.system(f'cp "{args.input_ann_file}" "{output_ann_file_path}"')

if __name__ == "__main__":
    main()
