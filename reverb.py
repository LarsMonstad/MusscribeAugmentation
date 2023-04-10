import os
import argparse
import numpy as np
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile

def apply_reverb(input_audio_file, output_audio_file, room_size, wet_level):
    with AudioFile(input_audio_file) as input_file:
        audio = input_file.read(input_file.frames)
        samplerate = input_file.samplerate

    reverb_effect = Reverb(room_size=room_size / 100.0, wet_level=wet_level / 100.0)
    pedalboard = Pedalboard([reverb_effect])

    processed_audio = pedalboard(audio, samplerate)

    with AudioFile(output_audio_file, 'w', samplerate, audio.shape[0]) as output_file:
        output_file.write(processed_audio)

def main():
    parser = argparse.ArgumentParser(description="Apply reverb to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("room_scale", type=float, help="Room scale (0 to 100)")
    parser.add_argument("reverberance", type=float, help="Reverberance (0 to 100)")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    input_filename = os.path.basename(args.input_audio_file)
    output_filename = os.path.splitext(input_filename)[0] + "_reverb" + os.path.splitext(input_filename)[1]
    output_file_path = os.path.join(args.output_directory, output_filename)

    apply_reverb(args.input_audio_file, output_file_path, args.room_scale, args.reverberance)

if __name__ == "__main__":
    main()
