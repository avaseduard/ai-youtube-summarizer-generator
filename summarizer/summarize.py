import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client with the API key
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# Summarize the transcribed text using ChatGPT
def summarize_text(chunks, output_file):
    summaries = []
    # Loop through each chunk of text and create a chat using OpenAI's API
    for chunk in chunks:
        completion = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = [
              {'role': 'system', 'content': 'You are a helpful assistant that summarizes youtube videos. You are provided chunks of raw audio that were transcribed from a youtube video. Summarize the current chunk to succint and clear bullet points of its contents.'},
              {'role': 'user', 'content': chunk}
            ]
          )
        # Extract the summary from the response
        summary = completion.choices[0].message.content
        # Append the summary to the list of summaries
        summaries.append(summary)
    # If an output_file is specified, save all summaries to a .txt file
    if output_file is not None:
        with open(output_file, 'w') as file:
            for summary in summaries:
                file.write(summary + '\n')
    # Return the list of summaries
    return summaries