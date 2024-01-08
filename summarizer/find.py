import os

# Find all files with .mp3 extension in path
def find_audio_files(path, extension='.mp3'):
    audio_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                # Put all .mp3 files paths in a list
                audio_files.append(os.path.join(root, file))
    return audio_files