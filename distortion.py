import os
import argparse
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment

def apply_distortion(audio_file, output_dir, gain):
    samples, sample_rate = librosa.load(audio_file, sr=None, mono=False)
    channels = samples.shape[0]

    input_audio = AudioSegment.from_file(audio_file, format='flac', channels=channels, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)
    
    output_audio = input_audio.apply_gain(gain)
    
    output_audio_file = os.path.join(output_dir, os.path.basename(audio_file))
    output_audio.export(output_audio_file, format='flac')

def main():
    parser = argparse.ArgumentParser(description="Apply distortion to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("gain", type=float, help="Gain for the distortion effect")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    apply_distortion(args.input_audio_file, args.output_directory, args.gain)

if __name__ == "__main__":
    main()
