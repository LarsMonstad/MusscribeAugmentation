import os
import argparse
import random
import string
from time_stretch import apply_time_stretch
from pitch_shift import apply_pitch_shift
from reverbfilter import apply_reverb_and_filters
from distortionchorus import apply_gain_and_chorus
from annmidi import ann_to_midi
from tqdm import tqdm

def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_output_filename(input_filename, effect_name, measure, random_suffix):
    return f"{os.path.splitext(input_filename)[0]}_{effect_name}_{measure}_{random_suffix}{os.path.splitext(input_filename)[1]}"

def convert_ann_files(directory):
    for filename in tqdm(os.listdir(directory), desc="Coverting ann to midi "):
        if filename.endswith(".ann"):
            ann_file_path = os.path.join(directory, filename)
            ann_to_midi(ann_file_path)
            # Call your conversion function here with ann_file_path as the argument
            # For example:
            # convert_ann_file(ann_file_path)

def main():
    parser = argparse.ArgumentParser(description="Apply audio effects to audio and annotation files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")

    args = parser.parse_args()

    # Use the input file's directory as the output directory
    output_directory = args.output_directory

    # Apply time stretch
    for i, stretch_factor in tqdm(enumerate([0.8, 1.2, 1.4]), desc="Time Stretch"):
        random_suffix = random_word(5)
        output_filename = generate_output_filename(os.path.basename(args.input_audio_file), "timestretch", stretch_factor, random_suffix)
        output_file_path = os.path.join(output_directory, output_filename)
        apply_time_stretch(args.input_audio_file, args.input_ann_file, output_file_path, stretch_factor)

    # Apply pitch shift
    for i, semitones in tqdm(enumerate([-2, 2, 4]), desc="Pitch Shift"):
        random_suffix = random_word(5)
        output_filename = generate_output_filename(os.path.basename(args.input_audio_file), "pitchshift", semitones, random_suffix)
        output_file_path = os.path.join(output_directory, output_filename)
        apply_pitch_shift(args.input_audio_file, args.input_ann_file, output_file_path, semitones)

    # Apply reverb and filters
    room_scales = [0, 30, 100]
    low_cutoffs = [20000, 16300, 17500]
    high_cutoffs = [20, 4000, 7000]

    for i, room_scale in tqdm(enumerate(room_scales), desc="Reverb and filter"):
        low_cutoff = random.choice(low_cutoffs)
        high_cutoff = random.choice(high_cutoffs)
        apply_reverb_and_filters(args.input_audio_file, args.input_ann_file, output_directory, room_scale, low_cutoff, high_cutoff)

    # Apply distortion
    depths = [0.2, 0.3, 0.5]
    chorusrates = [1, 2, 1]
    for i, gain in tqdm(enumerate([3, 5, 10]), desc= "Reverb and filter"):
        depth = random.choice(depths)
        chorusrate = random.choice(chorusrates)
        apply_gain_and_chorus(args.input_audio_file, args.input_ann_file, output_directory, gain, depth, chorusrate)

    convert_ann_files(output_directory)

if __name__ == "__main__":
    main()
