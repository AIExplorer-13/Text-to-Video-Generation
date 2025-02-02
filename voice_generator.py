import requests
import base64
from moviepy.editor import AudioFileClip
import re

ENDPOINT = 'https://tiktok-tts.weilnet.workers.dev/api/generation'
TEXT_CHAR_LIMIT = 299

def split_text(text: str, chunk_size: int):
    sentences = re.split(r'([.!?])', text)
    text_chunks = []
    current_chunk = ""
    for sentence in sentences:
        if (len(current_chunk) + len(sentence) <= chunk_size):
            current_chunk += ' ' + sentence
        else:
            if current_chunk:
                text_chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        text_chunks.append(current_chunk.strip())
    return text_chunks

def generate_voice(text: str):
    try:
        res = requests.post(url=ENDPOINT, json={
            'text': text, 'voice': 'en_us_001'
        })
        res.raise_for_status()
        return res.json()['data']
    except Exception as error:
        print('Error getting response from TikTok TTS API:', error)
        return None

def text_to_speech(text: str, audio_filepath: str):
    try:
        if len(text) <= TEXT_CHAR_LIMIT:
            encoded_audio = generate_voice(text)
        else:
            text_chunks = split_text(text, chunk_size=TEXT_CHAR_LIMIT)
            encoded_audio = ''.join([generate_voice(text_chunk) for text_chunk in text_chunks])

        if encoded_audio:
            audio_bytes = base64.b64decode(encoded_audio)
            with open(audio_filepath, 'wb') as file:
                file.write(audio_bytes)
            return AudioFileClip(audio_filepath)
        else:
            print("Error: No audio data returned.")
            return None
    except Exception as error:
        print("Error generating text to speech:", error)
        return None

if __name__ == '__main__':
    text = "It's not a lack of compassion; our minds often assume someone else will step in. Understanding this effect helps us realize the importance of taking personal responsibility in emergencies."
    audio_filepath = 'output/audio/voiceover.mp3'
    text_to_speech(text, audio_filepath)
