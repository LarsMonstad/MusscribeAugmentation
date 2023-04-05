import os
import argparse
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.effects import reverb

def apply_reverb(audio_file, output_dir, room_scale, reverberance):
    samples, sample_rate = librosa.load(audio_file, sr=None, mono=False)
    input_audio = AudioSegment.from_mono_audiosegments(
        AudioSegment.from_file(audio_file, format='flac', channels=1, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)[:samples.shape[1]],
        AudioSegment.from_file(audio_file, format='flac', channels=1, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)[samples.shape[1]:]
    )
    output_audio = reverb(input_audio, room_scale=room_scale, reverberance=reverberance)
    output_audio_file = os.path.join(output_dir, os.path.basename(audio_file))
    output_audio.export(output_audio_file, format='flac')

def main():
    parser = argparse.ArgumentParser(description="Apply reverb to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("room_scale", type=float, help="Room scale (0 to 100)")
    parser.add_argument("reverberance", type=float, help="Reverberance (0 to 100)")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    apply_reverb(args.input_audio_file, args.output_directory, args.room_scale, args.reverberance)

if __name__ == "__main__":
    main()
