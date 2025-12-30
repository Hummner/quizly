import json
import yt_dlp
import whisper
import subprocess
from google import genai
import os




class AudioConverter():

    def __init__(self, url, username):
        self.url = url
        self.username = username
        self.input_audio = None
        self.TMP_AUDIO = f"media/{self.username}/whisper_audio_{self.username}.wav"

    def run(self):
        try:
            self.youtube_download()
            self.convert_audio()
            text = self.whisper()
            return self.gemini_api(text)
        
        except Exception as e:
            print(f"Fehler in run(): {e}")
            raise  # wirft GENAU den gleichen Fehler erneut

        finally:
            self.cleanup()

    def youtube_download(self):
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
        model = whisper.load_model("turbo")
        result = model.transcribe(self.TMP_AUDIO)
        text = result["text"]
        return text
    
    def gemini_api(self, text):
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
            model="gemini-2.5-flash", contents=promp
        )

        
        return response.text
    
    def cleanup(self):
        for path in [self.input_audio, self.TMP_AUDIO]:
            os.remove(path)

        user_dir = f"media/{self.username}"
        if os.path.isdir(user_dir) and not os.listdir(user_dir):
            os.rmdir(user_dir)


new_object = AudioConverter(url = 'https://www.youtube.com/watch?v=GU81TzgPENA', username="bence")


quiz = new_object.run()
with open("quiz_test.txt", "w", encoding="utf-8") as f:
    f.write(quiz)


