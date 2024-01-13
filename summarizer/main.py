import os, shutil
from flask import Flask, jsonify, request
from flask_cors import CORS
from download import download_video_info
from split import split_audio_file
from transcribe import transcribe_audio_files
from summarize import summarize_text

app = Flask(__name__)
# CORS settings
CORS(app, resources={r"/get_summary": {"origins": "*", "methods": ["POST"], "allow_headers": "*"}})
# POST request
@app.route('/get_summary', methods=['POST'])
# Get youtube video's summary, thumbnail, title and send to front end
def get_summary():
    def summarize_youtube_video(youtube_url, outputs_dir):
        raw_audio_dir = f"{outputs_dir}/raw_audio/"
        segments_dir = f"{outputs_dir}/segments"
        transcripts_file = f"{outputs_dir}/transcripts.txt"
        summary_file = f"{outputs_dir}/summary.txt"
        # Chunk to 10 min segments
        segment_length = 10 * 60
        # Delete the outputs folder and start from scratch
        if os.path.exists(outputs_dir):
            shutil.rmtree(outputs_dir)
            os.mkdir(outputs_dir)
        # Download the audio using youtube_dlp
        audio_path, thumbnail_url, video_title = download_video_info(youtube_url, raw_audio_dir)
        # audio_filename = download_audio(youtube_url, raw_audio_dir)
        # Split each audio file
        chunked_audio_files = split_audio_file(audio_path, segment_length, segments_dir)
        # Transcribe each splitted audio file using Whisper
        transcriptions = transcribe_audio_files(chunked_audio_files, transcripts_file)
        # Summarize each transcription using chatGPT
        summaries = summarize_text(transcriptions, summary_file)
        # Put the entire summary into a single entry
        final_summary = '\n'.join(summaries)
        # Return the complete summary in text, the thumbnail's url and the title string
        return final_summary, thumbnail_url, video_title
    # Set parameters
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    outputs_dir = 'outputs/'
    # Call summarize function
    final_summary, thumbnail_url, video_title = summarize_youtube_video(youtube_url, outputs_dir)
    # Send json info to front end
    return jsonify({'summary': final_summary, 'thumbnail_url': thumbnail_url, 'video_title': video_title})

if __name__ == '__main__':
    app.run(debug=True)
