# import yt_dlp
# import os
# from find import find_audio_files

# # Download the audio from a youtube video, save it to output_dir as an .mp3 file and return the filename
# def download_audio(video_url, output_path):
#     # Youtube-dlp download options
#     ydlp_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
#     }
#     # If output folder doesn't exist, create it
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
#     # Download audio from youtube video using options
#     with yt_dlp.YoutubeDL(ydlp_opts) as ydl:
#         ydl.download([video_url])
#     # Select audio file from folder
#     audio_filename = find_audio_files(output_path)[0]
#     # Return name of audio file
#     return audio_filename