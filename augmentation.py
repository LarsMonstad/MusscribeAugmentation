import os
import argparse
from time_stretch import apply_time_stretch
from pitch_shift import apply_pitch_shift
from reverb import apply_reverb
from distortion import apply_distortion

def main():
    parser = argparse.ArgumentParser(description="Apply audio effects to audio and annotation files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    # Apply time stretch
    for i, stretch_factor in enumerate([0.8, 1.2, 1.4]):
        output_subdir = os.path.join(args.output_directory, f"timestretch_{i+1}")
        apply_time_stretch(args.input_audio_file, args.input_ann_file, output_subdir, stretch_factor)

    # Apply pitch shift
    for i, semitones in enumerate([-2, 2, 4]):
        output_subdir = os.path.join(args.output_directory, f"pitchshift_{i+1}")
        apply_pitch_shift(args.input_audio_file, args.input_ann_file, output_subdir, semitones)

    # Apply reverb
    for i, room_scale in enumerate([0.3, 0.6, 0.9]):
        output_subdir = os.path.join(args.output_directory, f"reverb_{i+1}")
        apply_reverb(args.input_audio_file, output_subdir, room_scale)

    # Apply distortion
    for i, gain in enumerate([10, 20, 30]):
        output_subdir = os.path.join(args.output_directory, f"distortion_{i+1}")
        apply_distortion(args.input_audio_file, output_subdir, gain)

if __name__ == "__main__":
    main()
