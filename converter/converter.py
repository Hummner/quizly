import json
import yt_dlp
import whisper
import subprocess
from google import genai
import os
import re


class AudioConverter():
    """
    Converts a YouTube video into a quiz JSON.

    Pipeline:
    - Download audio from YouTube (yt_dlp)
    - Convert audio to a Whisper-friendly WAV format (ffmpeg)
    - Transcribe speech to text (Whisper)
    - Send transcript to Gemini to generate quiz JSON
    - Clean and parse the JSON
    - Remove temporary files
    """

    def __init__(self, url, username):
        """
        Initializes the converter.

        - url: YouTube video URL
        - username: used to build user-specific temp file paths
        - input_audio: path to the downloaded audio file (set later)
        - TMP_AUDIO: path to the converted WAV file for Whisper
        """
        self.url = url
        self.username = username
        self.input_audio = None
        self.TMP_AUDIO = f"media/{self.username}/whisper_audio_{self.username}.wav"

    def run(self):
        """
        Executes the full conversion process.

        Steps:
        - Download audio from YouTube
        - Convert audio to WAV (mono, 16kHz)
        - Transcribe with Whisper
        - Generate quiz JSON with Gemini
        - Remove Markdown code fences if present
        - Parse JSON and return it as a Python dict

        Always runs cleanup at the end (even on errors).
        """
        try:
            self.youtube_download()
            self.convert_audio()
            text = self.whisper()
            gemini_respond = self.gemini_api(text)
            clean_text = self.strip_code_fence(gemini_respond)
            return json.loads(clean_text)

        except Exception as e:
            print(f"Fehler in run(): {e}")
            raise

        finally:
            self.cleanup()

    def youtube_download(self):
        """
        Downloads the best available audio stream from YouTube.

        - Saves it into a user-specific media folder
        - Stores the final downloaded filename in self.input_audio
        """
        tmp_filename = f"media/{self.username}/temp_audio_{self.username}.%(ext)s"
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": tmp_filename,
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Download: Beginn")
            info = ydl.extract_info(self.url, download=True)
            self.input_audio = ydl.prepare_filename(info)

    def convert_audio(self):
        """
        Converts the downloaded audio into a WAV file optimized for Whisper.

        Uses ffmpeg to:
        - overwrite existing output (-y)
        - convert to mono (-ac 1)
        - resample to 16 kHz (-ar 16000)
        """
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", self.input_audio,
                "-ac", "1",
                "-ar", "16000",
                self.TMP_AUDIO,
            ],
            check=True
        )

    def whisper(self):
        """
        Transcribes the WAV file into text using Whisper.

        Loads the Whisper 'turbo' model and returns the transcript text.
        """
        model = whisper.load_model("turbo")
        result = model.transcribe(self.TMP_AUDIO)
        text = result["text"]
        return text

    def gemini_api(self, text):
        """
        Sends the transcript to Gemini and requests a quiz in strict JSON format.

        The prompt enforces:
        - JSON only (no extra text)
        - 10 questions
        - 4 options per question
        - exactly one correct answer matching one of the options
        """
        client = genai.Client()
        promp = f"""{text} --->
                        Based on the following transcript, generate a quiz in valid JSON format.

                    The quiz must follow this exact structure:

                    {{

                    "title": "Create a concise quiz title based on the topic of the transcript.",

                    "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",

                    "questions": [

                        {{

                        "question_title": "The question goes here.",

                        "question_options": ["Option A", "Option B", "Option C", "Option D"],

                        "answer": "The correct answer from the above options"

                        }},

                        ...

                        (exactly 10 questions)

                    ]

                    }}

                    Requirements:

                    - Each question must have exactly 4 distinct answer options.

                    - Only one correct answer is allowed per question, and it must be present in 'question_options'.

                    - The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).

                    - Do not include explanations, comments, or any text outside the JSON.
                    """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=promp
        )

        return response.text

    def cleanup(self):
        """
        Deletes temporary audio files and removes the user folder if empty.

        Runs in 'finally' to ensure temp files are removed even if an error occurs.
        """
        for path in [self.input_audio, self.TMP_AUDIO]:
            os.remove(path)

        user_dir = f"media/{self.username}"
        if os.path.isdir(user_dir) and not os.listdir(user_dir):
            os.rmdir(user_dir)

    def strip_code_fence(self, text: str):
        """
        Removes Markdown code fences from the Gemini output.

        Example it handles:
        ```json
        {...}
        ```
        """
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()
