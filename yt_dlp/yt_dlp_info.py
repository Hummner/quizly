import json
import yt_dlp
import whisper
import subprocess




class AudioConverter():

    def __init__(self, url):
        self.url = url
        self.TMP_AUDIO = "media/temp_audio.mp3"

    def youtube_download(self):
        tmp_filename = "media/temp_audio.%(ext)s"
        ydl_opts = {

            "format": "bestaudio/best",

            "outtmpl": tmp_filename,

            "quiet": True,

            "noplaylist": True,


        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print('Download: Beginn')
            ydl.download([self.url])
        
        return self.convert_audio()
    
    def convert_audio(self):
        input_audio = "media/temp_audio.webm"
        output_audio = "media/whisper_audio.wav"
        
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", input_audio,
                "-ac", "1",
                "-ar", "16000",
                output_audio,
            ],
            check=True
        )

    def whisper(self):
        model = whisper.load_model("turbo")
        result = model.transcribe(self.TMP_AUDIO)
        text = result["text"]
        return text[:50]


new_object = AudioConverter(url = 'https://www.youtube.com/watch?v=GU81TzgPENA')


new_object.convert_audio()
text = new_object.whisper()

print(text)



