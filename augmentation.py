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
from add_pauses import calculate_time_distance

def delete_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_output_filename(input_filename, effect_name, measure, random_suffix):
    return f"{os.path.splitext(input_filename)[0]}_{effect_name}_{measure}_{random_suffix}{os.path.splitext(input_filename)[1]}"

def main():
    parser = argparse.ArgumentParser(description="Apply audio effects to audio and annotation files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")

    args = parser.parse_args()

    output_directory = args.output_directory
    isExist = os.path.exists(output_directory)
    if not isExist:
        os.makedirs(output_directory)

    #create a list of ann files 
    new_ann_files = []
    # Apply pauses #to do add pausefactor
    pausesfactor = 1
    random_suffix = random_word(5)
    output_filename = generate_output_filename(os.path.basename(args.input_audio_file), "addpauses", pausesfactor, random_suffix)
    output_file_path = os.path.join(output_directory, output_filename)
    output_ann_filep = calculate_time_distance(args.input_audio_file, args.input_ann_file, output_file_path)
    if output_ann_filep!="Silent":
        new_ann_files.append(output_ann_filep)


    generated_stretch_factors = set()
    for _ in tqdm(range(3), desc="Time Stretch"):
        stretch_factor = 1
        while stretch_factor == 1 or stretch_factor in generated_stretch_factors:
            stretch_factor = round(random.uniform(0.6, 1.6), 1)
        generated_stretch_factors.add(stretch_factor)
        random_suffix = random_word(5)
        output_filename = generate_output_filename(os.path.basename(args.input_audio_file), "timestretch", stretch_factor, random_suffix)
        output_file_path = os.path.join(output_directory, output_filename)
        output_ann_file = apply_time_stretch(args.input_audio_file, args.input_ann_file, output_file_path, stretch_factor)
        new_ann_files.append(output_ann_file)


    generated_semitones = set()
    for _ in tqdm(range(3), desc="Pitch Shift"):
        semitones = 0
        while semitones == 0 or semitones in generated_semitones:
            semitones = random.choice([n for n in range(-5, 5) if n != 0])
        generated_semitones.add(semitones)
        random_suffix = random_word(5)
        output_filename = generate_output_filename(os.path.basename(args.input_audio_file), "pitchshift", semitones, random_suffix)
        output_file_path = os.path.join(output_directory, output_filename)
        output_ann_file = apply_pitch_shift(args.input_audio_file, args.input_ann_file, output_file_path, semitones)
        new_ann_files.append(output_ann_file)


    generated_roomscales = set()
    cutoff_pairs = [(20, 20000), (300, 20000), (3000, 20000),(20, 16300), (20, 17500), (20, 18000)]
    for _ in tqdm(range(3), desc="Reverb and filter"):
        room_scale = 0
        while room_scale == 0 or room_scale in generated_roomscales:
            room_scale = random.choice([n for n in range(10,100)])
        generated_roomscales.add(room_scale)
        high_cutoff, low_cutoff  = random.choice(cutoff_pairs)
        output_ann_file = apply_reverb_and_filters(args.input_audio_file, args.input_ann_file, output_directory, room_scale, low_cutoff, high_cutoff)
        new_ann_files.append(output_ann_file)


    chorusrates = [1, 1, 1]
    generated_depths = set()
    generated_gains = set()
    for _ in tqdm(range(3), desc= "gain and chorusrate"):
        depth = 0
        gain = 0 
        while depth == 0 or depth in generated_depths:
            depth = round(random.uniform(0.1, 0.6), 1)
        generated_depths.add(depth)
        while gain == 0 or gain in generated_gains:
            gain = random.choice([n for n in range(2, 11)])
        generated_gains.add(gain)
        chorusrate = random.choice(chorusrates)
        output_ann_file = apply_gain_and_chorus(args.input_audio_file, args.input_ann_file, output_directory, gain, depth, chorusrate)
        new_ann_files.append(output_ann_file)

    #convert_ann_files(output_directory)
    for ann_file in tqdm(new_ann_files, desc= "Converting ann files to midi"):
        ann_to_midi(ann_file)
        delete_file(ann_file)

if __name__ == "__main__":
    main()
