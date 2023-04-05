#based on the COMPOSER CLASSIFICATION WITH CROSS-MODAL TRANSFER LEARNING AND MUSICALLY-INFORMED AUGMENTATION article at ismir 
#removes colomuns/phrases of notes with a pause threshold to avoid cutting off. Uses the ANN file to detect which notes to remove and mutes the same part from the audio 
import sys
import random
import librosa
import numpy as np
import os
import soundfile as sf

def extract_suitable_segments(annotation_data, pause_threshold=0.15):
    """
    Identify suitable segments for removal based on pauses.
    """
    suitable_segments = []
    prev_offset = 0

    for line in annotation_data:
        onset, offset, _, _ = map(float, line.strip().split('\t'))
        pause_duration = onset - prev_offset

        if pause_duration >= pause_threshold:
            suitable_segments.append((prev_offset, onset))
        
        prev_offset = offset

    return suitable_segments

def remove_random_segment(annotation_data, audio_data, sample_rate, pause_threshold=0.15):
    suitable_segments = extract_suitable_segments(annotation_data, pause_threshold)
    
    if not suitable_segments:
        return audio_data, annotation_data

    # Select a random segment for removal
    random_segment = random.choice(suitable_segments)
    start_time, end_time = random_segment

    # Print the duration of the removed segment
    removed_duration = end_time - start_time
    print(f"Removed segment duration: {removed_duration:.2f} seconds")

    # Remove the segment from the audio
    start_sample = librosa.time_to_samples(start_time, sr=sample_rate)
    end_sample = librosa.time_to_samples(end_time, sr=sample_rate)
    audio_data = np.concatenate((audio_data[:start_sample], audio_data[end_sample:]))

    # Remove the segment from the annotation data
    new_annotation_data = []
    for line in annotation_data:
        onset, offset, pitch, velocity = map(float, line.strip().split('\t'))
        if onset < start_time or onset > end_time:
            new_annotation_data.append(line)

    return audio_data, new_annotation_data

def process_audio_and_annotations(ann_filename, audio_filename):
    audio_data, sample_rate = librosa.load(audio_filename, sr=None)

    with open(ann_filename, 'r') as ann_file:
        annotation_data = ann_file.readlines()

    new_audio_data, new_annotation_data = remove_random_segment(annotation_data, audio_data, sample_rate)

    # Save the new audio file
    output_audio_filename = os.path.splitext(audio_filename)[0] + '_removed_segment.flac'
    sf.write(output_audio_filename, new_audio_data, sample_rate)

    # Save the new annotation file
    output_ann_filename = os.path.splitext(ann_filename)[0] + '_removed_segment.ann'
    with open(output_ann_filename, 'w') as output_ann_file:
        output_ann_file.writelines(new_annotation_data)

def main(ann_filename, audio_filename):
    process_audio_and_annotations(ann_filename, audio_filename)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} ann_file audio_file")
        sys.exit(1)

    ann_filename = sys.argv[1]
    audio_filename = sys.argv[2]

    main(ann_filename, audio_filename)
