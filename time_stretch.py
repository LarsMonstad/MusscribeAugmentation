import os
import sys
import argparse
import random
import librosa
import numpy as np
import soundfile as sf
# Load the annotations
def load_ann_file(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    return [line.strip() for line in content]

# Save the updated annotations
def save_ann_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write('\n'.join(content))

# Update the annotation timestamps
def update_ann_file(ann_content, stretch_factor):
    updated_content = []
    for line in ann_content:
        parts = line.strip().split('\t')
        onset, offset, pitch, channel = parts
        onset_new = float(onset) / stretch_factor
        offset_new = float(offset) / stretch_factor
        updated_line = f"{onset_new:.3f}\t{offset_new:.3f}\t{pitch}\t{channel}"
        updated_content.append(updated_line)
    return updated_content



# Apply time stretch to audio and annotation files
def apply_time_stretch(audio_file, ann_file, output_dir, stretch_factor):
    # Load audio file
    samples, sample_rate = librosa.load(audio_file, sr=None, mono=False)

    # Apply the time-stretch transformation directly
    time_stretched_samples = librosa.effects.time_stretch(samples, rate=stretch_factor)
    #time_stretched_samples = librosa.effects.time_stretch(samples, rate=1/stretch_factor)


    # Print input and output shapes and the stretch factor
    print(f"Input samples shape: {samples.shape}")
    print(f"Output samples shape: {time_stretched_samples.shape}")
    print(f"Stretch factor: {stretch_factor}")

    # Save the time-stretched audio
    output_audio_file = os.path.join(output_dir, os.path.basename(audio_file))
    sf.write(output_audio_file, time_stretched_samples.T, sample_rate, format='flac')

    # Update and save the time-stretched annotations
    ann_content = load_ann_file(ann_file)
    updated_ann_content = update_ann_file(ann_content, stretch_factor)
    output_ann_file = os.path.join(output_dir, os.path.basename(ann_file))
    save_ann_file(output_ann_file, updated_ann_content)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Time-stretch audio and annotation files")
    parser.add_argument(
        "input_audio_file", help="Path to the input audio file (FLAC or WAV)"
    )
    parser.add_argument("input_ann_file", help="Path to the input annotation file (.ann)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument(
        "stretch_factor",
        type=float,
        help="Time stretch factor (e.g., 1.4 for 40% faster, 0.8 for 20% slower)",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Make sure the output directory exists
    os.makedirs(args.output_directory, exist_ok=True)

    # Apply time stretch to audio and annotation files
    apply_time_stretch(
        args.input_audio_file,
        args.input_ann_file,
        args.output_directory,
        args.stretch_factor,
    )

if __name__ == "__main__":
    main()
# Examp

