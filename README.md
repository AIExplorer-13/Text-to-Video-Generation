# shorts-generator
A script that generates short videos with voice-over narration, background images and subtitles.

# How it works
- Generates a script using Google's Gemini AI API
  - The content of the script is controlled by the prompt found in `prompt.txt`
  - Feel free to try modifying the prompt to generate scripts with different types of content
  - However, do not modify the part of the prompt that controls the output format of the response, as doing so will likely break the script
- Generates voice-over narration of the script using Tiktok's unofficial text-to-speech API
- Fetches stock photos from Pexels API using search terms that are also generated by Gemini
- Compiles stock photos into a video using moviepy
- Generates subtitles with timestamps in .srt format using the AssemblyAI speech-to-text API
- Burns subtitles into the video and adds the voice-over audio using moviepy

# Getting started
## Obtaining required API keys
Obtain API keys for the following:
- [Google Gemini API](https://aistudio.google.com/app/apikey)
- [Pexels API](https://pexels.com/api)
- [AssemblyAI API](https://assemblyai.com/pricing)
## Installation and setup
1. Clone the repository and navigate to the project directory
```
git clone https://github.com/Glenn-Chiang/shorts-generator.git
cd shorts-generator
```
2. Create a `.env` file and fill in the values for the required API keys. Refer to `.env.example`.
3. Create a virtual environment and install dependencies
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
## Manage assets (optional)
The `assets/video` folder contains video files that the script will randomly select from to use as background clips. Feel free to add your own video files under this folder.
## Usage
```
python main.py
```

# Disclaimer
This project relies on experimental generative AI technology which may occasionally produce malformed output that breaks the script.
