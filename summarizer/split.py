import os, librosa
import soundfile as sf
from find import find_audio_files

# Split long audio files to fit Whisper and ChatGPT limits
def split_audio_file(filename, segment_length, output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    # Load audio file
    audio, sr = librosa.load(filename, sr=44100)
    # Get duration in seconds
    duration = librosa.get_duration(y=audio, sr=sr)
    # Compute number of segments
    segments = int(duration / segment_length) + 1
    # Save segments
    for i in range(segments):
        start = i * segment_length * sr
        end = (i + 1) * segment_length * sr
        segment = audio[start:end]
        sf.write(os.path.join(output_dir, f"segment_{i}.mp3"), segment, sr)
    # Find all splitted files
    splitted_audio_files = find_audio_files(output_dir)
    # Return a sorted list of splitted audio files
    return sorted(splitted_audio_files)