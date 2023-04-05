#based on the COMPOSER CLASSIFICATION WITH CROSS-MODAL TRANSFER LEARNING AND MUSICALLY-INFORMED AUGMENTATION article at ismir 
#removes colomuns/phrases of notes with a pause threshold to avoid cutting off. Uses the ANN file to detect which notes to remove and mutes the same part from the audio 
# not fixed! 
import sys
import librosa
import numpy as np
import os
import soundfile as sf
import random

def has_suitable_pauses(segment, segments, min_pause_duration=0.05, max_distance=100, min_segment_duration=2):
    onset, offset = segment
    if offset - onset < min_segment_duration:
        return False

    prev_pause = None
    next_pause = None
    
    for s_onset, s_offset in segments:
        if s_offset >= onset:
            break

        if prev_pause is None or onset - s_offset < onset - prev_pause:
            prev_pause = s_offset

    for s_onset, s_offset in segments:
        if s_onset > offset:
            if next_pause is None or s_onset - offset < next_pause - offset:
                next_pause = s_onset
            break

    if prev_pause is None or next_pause is None:
        return False

    return (
        (onset - prev_pause >= min_pause_duration) and
        (next_pause - offset >= min_pause_duration) and
        (next_pause - prev_pause <= max_distance)
    )



def remove_segments_and_mute_audio(ann_filename, audio_filename, max_segments_per_minute=50):
    audio_data, sample_rate = librosa.load(audio_filename, sr=None)
    mute_mask = np.ones_like(audio_data)

    segments_removed = 0
    total_removed_duration = 0

    with open(ann_filename, 'r') as ann_file:
        lines = [line.strip().split('\t') for line in ann_file]
        segments = [(float(onset), float(offset)) for onset, offset, _, _ in lines]

    suitable_segments = []
    prev_offset = 0
    for i, (onset, offset) in enumerate(segments[:-1]):
        if has_suitable_pauses((onset, offset), segments):
            suitable_segments.append((onset, offset))
        else:
            print(f"Not suitable: {onset}, {offset}")

    segments_by_minute = {}
    for start, end in suitable_segments:
        minute = int(start // 60)
        if minute not in segments_by_minute:
            segments_by_minute[minute] = []
        segments_by_minute[minute].append((start, end))

    removed_segments = []

    for minute, segment_list in segments_by_minute.items():
        segments_to_remove = min(max_segments_per_minute, len(segment_list))
        removed_segments_minute = random.sample(segment_list, segments_to_remove)
        removed_segments.extend(removed_segments_minute)

        for start, end in removed_segments_minute:
            start_sample = librosa.time_to_samples(start, sr=sample_rate)
            end_sample = librosa.time_to_samples(end, sr=sample_rate)
            mute_mask[start_sample:end_sample] = 0
            total_removed_duration += (end - start)
            segments_removed += 1

    muted_audio_data = audio_data * mute_mask
    output_audio_filename = os.path.splitext(audio_filename)[0] + '_removed_segments.flac'
    sf.write(output_audio_filename, muted_audio_data, sample_rate)

    print(f"Removed segments: {segments_removed}")
    print(f"Total removed duration: {total_removed_duration:.2f} seconds")

    output_ann_data = []
    for i, line in enumerate(lines):
        onset, offset = segments[i]
        if not any(start <= onset < end for start, end in removed_segments):
            output_ann_data.append('\t'.join(line) + '\n')

    output_ann_filename = os.path.splitext(ann_filename)[0] + '_removed_segments.ann'
    with open(output_ann_filename, 'w') as output_ann_file:
        output_ann_file.writelines(output_ann_data)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} ann_file audio_file")
        sys.exit(1)

    ann_filename = sys.argv[1]
    audio_filename = sys.argv[2]

    remove_segments_and_mute_audio(ann_filename, audio_filename)

