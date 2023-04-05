import os
import argparse
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from audiotsm import audio_effects

def apply_distortion(audio_file, output_dir, gain):
    samples, sample_rate = librosa.load(audio_file, sr=None, mono=False)
    input_audio = AudioSegment.from_mono_audiosegments(
        AudioSegment.from_file(audio_file, format='flac', channels=1, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)[:samples.shape[1]],
        AudioSegment.from_file(audio_file, format='flac', channels=1, frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8)[samples.shape[1]:]
    )

    samples = np.array(input_audio.get_array_of_samples()).reshape(-1, 2).T
    distorted_samples = audio_effects.overdrive(samples, gain)
    output_audio = AudioSegment(distorted_samples.tobytes(), frame_rate=sample_rate, sample_width=samples.dtype.itemsize * 8, channels=2)
    
    output_audio_file = os.path.join(output_dir, os.path.basename(audio_file))
    output_audio.export(output_audio_file, format='flac')

def main():
    parser = argparse.ArgumentParser(description="Apply distortion to audio files")
    parser.add_argument("input_audio_file", help="Path to the input audio file (FLAC or WAV)")
    parser.add_argument("output_directory", help="Path to the output directory")
    parser.add_argument("gain", type=float, help="Gain for the overdrive effect")

    args = parser.parse_args()

    os.makedirs(args.output_directory, exist_ok=True)

    apply_distortion(args.input_audio_file, args.output_directory, args.gain)

if __name__ == "__main__":
    main()
