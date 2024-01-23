import os
import yt_dlp
from find import find_audio_files

# Get audio file path, thumbnail url and video title
def download_video_info(video_url, output_directory):
    # Set up the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    # Set up the yt_dlp options
    ydlp_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        'writethumbnail': True,
    }
    # Download audio, get thumbnail and title
    with yt_dlp.YoutubeDL(ydlp_opts) as ydl:
        # Get video information
        info_dict = ydl.extract_info(video_url, download=False)
        ydl.download([video_url])
        # Select audio file from folder
        audio_path = find_audio_files(output_directory)[0]
        # Get thumbnail URL
        thumbnail_url = f"https://img.youtube.com/vi/{info_dict['id']}/sddefault.jpg"
        # Get video title
        video_title = info_dict.get('title', '')
    return audio_path, thumbnail_url, video_title