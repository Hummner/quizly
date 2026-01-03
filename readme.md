# Quizly 🎥🧠

Quizly is a Django web application that automatically generates an AI-powered quiz from a YouTube video.  
Quiz questions are created using **Google Gemini**, while **FFmpeg** is used for audio and video processing.

---

## Features

- Generate quizzes from YouTube videos  
- AI-powered question generation using Google Gemini  
- Strict JSON output format  
- FFmpeg support for audio and video processing  
- Local development setup  

---

## Requirements

- Python **3.10 or higher**
- pip
- FFmpeg
- Google Gemini API Key

---

# Setup (Windows)

## 1. Install FFmpeg

FFmpeg is required for processing video and audio files.

### Installation

1. Download FFmpeg (for example from gyan.dev or BtbN builds)
2. Extract it to:
   ```
   C:\ffmpeg\
   ```
3. Make sure the following file exists:
   ```
   C:\ffmpeg\bin\ffmpeg.exe
   ```

### Add FFmpeg to PATH

1. Open **Start Menu** → search for **Environment Variables**
2. Click **Edit the system environment variables**
3. Click **Environment Variables...**
4. Under **User variables** or **System variables**, select `Path` → **Edit**
5. Click **New** and add:
   ```
   C:\ffmpeg\bin
   ```
6. Save and restart your terminal

### Verify installation
```cmd
ffmpeg -version
```

---

## 2. Create a Gemini API Key

1. Open Google AI Studio  
   https://aistudio.google.com/
2. Sign in with your Google account
3. Click **Get API key** or **Create API key**
4. Create a new API key
5. Copy the key

⚠️ Important:
- Never share your API key
- Never commit your API key to GitHub

---

## 3. Clone the repository

```bash
git clone https://github.com/Hummner/quizly.git .
```

---

## 4. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Create a `.env` file

Create a `.env` file in the **project root**:

```
quizly/
├── .env
├── manage.py
├── requirements.txt
└── ...
```

### `.env` content
```env
GEMINI_API_KEY=your_api_key_here
```

---

## 7. Django setup

### Apply migrations
```bash
python manage.py migrate
```

### Create superuser (optional)
```bash
python manage.py createsuperuser
```

### Run development server
```bash
python manage.py runserver
```

Open in your browser:
```
http://127.0.0.1:8000/
```

---

# Setup (macOS / Linux)

## 1. Install FFmpeg

### macOS (Homebrew)
```bash
brew install ffmpeg
ffmpeg -version
```

### Linux (Debian / Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

---

## 2. Create a Gemini API Key

1. Open Google AI Studio  
   https://aistudio.google.com/
2. Sign in and create an API key
3. Copy the key

---

## 3. Clone the repository

```bash
git clone https://github.com/Hummner/quizly.git .
```

---

## 4. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Create `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 7. Run Django

```bash
python manage.py migrate
python manage.py runserver
```

---

## Common Issues

### FFmpeg not found (Windows)
```cmd
where ffmpeg
```
- Ensure `C:\ffmpeg\bin` is in your PATH
- Restart the terminal

---

### `.env` file not loaded
- Make sure `.env` is in the project root
- Ensure `python-dotenv` is installed
- Restart the Django server
