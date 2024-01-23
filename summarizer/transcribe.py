import os
import concurrent.futures
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Transcribe the audio files of the video
def transcribe_audio_files(audio_files, output_file):
    transcripts = []
    # Open all audio files outside the loop
    audio_file_handles = [open(file, 'rb') for file in audio_files]
    # Send batch files to transcribe with Open AI Whisper model
    def transcribe_audio_file(audio_file_handle):
        return client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file_handle,
            response_format='text'
        )
    # Use async requests and parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use batch processing with asynchronous requests
        future_to_audio = {executor.submit(transcribe_audio_file, audio_file_handle): audio_file_handle
                           for audio_file_handle in audio_file_handles}
        # 
        for future in concurrent.futures.as_completed(future_to_audio):
            audio_file_handle = future_to_audio[future]
            try:
                transcript = future.result()
                transcripts.append(transcript)
            except Exception as e:
                print(f"Error processing audio file {audio_file_handle.name}: {e}")
    # Close audio files after transcription
    for audio_file_handle in audio_file_handles:
        audio_file_handle.close()
    # If an output file is specified, save all transcripts to a .txt file
    if output_file is not None:
        with open(output_file, 'w') as file:
            for transcript in transcripts:
                file.write(transcript + '\n')
    # Return the list of transcripts
    return transcripts