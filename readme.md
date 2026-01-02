# Quizly 🎥🧠

Quizly is a Django web application that generates an AI-powered quiz from a YouTube video.

---

## Features
- Generate quizzes from YouTube videos
- AI-powered question generation using Gemini
- Local development setup
- FFmpeg support for audio/video processing

---

## Requirements
- Python 3.10 or higher
- pip
- FFmpeg
- Gemini API Key (`GEMINI_API_KEY`)

---

## How to get a Gemini API Key

Quizly uses Google Gemini for AI-powered quiz generation.  
You need a Gemini API key to use this feature.

### Steps

1. Open the Google AI Studio:
   https://aistudio.google.com/

2. Sign in with your Google account.

3. Click on **“Get API key”** or **“Create API key”**.

4. Create a new API key for your project.

5. Copy the generated key.

6. Set the key as an environment variable called: GEMINI_API_KEY

⚠️ **Important**
- Do not share your API key publicly.
- Never commit your API key to GitHub.
- Always use environment variables for secrets.


## Installation (Localhost)

### 1. Clone the repository (Windows)
```cmd
git clone https://github.com/Hummner/quizly.git .
```

---

### 2. Create and activate a virtual environment

#### Windows (CMD)
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies
```cmd
pip install -r requirements.txt
```

---

## Environment Variables

Quizly requires a Gemini API key stored in an environment variable.

### GEMINI_API_KEY

#### Windows (CMD) - Temporary
```cmd
set GEMINI_API_KEY=your_api_key_here
```

#### Windows (CMD) - Permanent
1. Open **Start Menu** → search **Environment Variables**
2. Click **Edit the system environment variables**
3. Click **Environment Variables...**
4. Under **User variables**, click **New**
   - Name: `GEMINI_API_KEY`
   - Value: `your_api_key_here`
5. Confirm with **OK**

Restart your terminal after setting the variable.

---

#### macOS / Linux - Temporary
```bash
export GEMINI_API_KEY="your_api_key_here"
```

#### macOS / Linux - Permanent
Add this line to `~/.bashrc`, `~/.zshrc`, or `~/.profile`:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Reload:
```bash
source ~/.bashrc
```

---

### Verify environment variable

#### Windows
```cmd
echo %GEMINI_API_KEY%
```

#### macOS / Linux
```bash
echo $GEMINI_API_KEY
```

---

## FFmpeg Installation

FFmpeg is required for processing video and audio files.

---

### Windows

1. Download FFmpeg (e.g. gyan.dev or BtbN builds)
2. Extract to:
   ```
   C:\ffmpeg\
   ```
3. Make sure this file exists:
   ```
   C:\ffmpeg\bin\ffmpeg.exe
   ```

#### Add FFmpeg to PATH
1. Open **Environment Variables**
2. Under **User variables** or **System variables**, select `Path`
3. Click **Edit** → **New**
4. Add:
   ```
   C:\ffmpeg\bin
   ```
5. Save and restart CMD

#### Verify
```cmd
ffmpeg -version
```

---

### macOS
```bash
brew install ffmpeg
ffmpeg -version
```

---

### Linux (Debian / Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

---

## Django Setup

### Apply migrations
```bash
python manage.py migrate
```

---

### Create superuser (optional)
```bash
python manage.py createsuperuser
```

---

### Run development server
```bash
python manage.py runserver
```

Open in browser:
```
http://127.0.0.1:8000/
```

---

## Common Issues

### FFmpeg not found (Windows)
- Ensure `C:\ffmpeg\bin` is in PATH
- Restart the terminal
- Verify:
```cmd
where ffmpeg
```

---

### GEMINI_API_KEY not found
- Check if the variable is set
```cmd
echo %GEMINI_API_KEY%
```
or
```bash
echo $GEMINI_API_KEY
```

---

## Notes
- Do not commit API keys to version control
- Use environment variables for secrets

---