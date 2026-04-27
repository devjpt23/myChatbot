# Voice Pizza Ordering Chatbot

A Python voice chatbot that acts as **"Bob the pizza guy"** and handles pizza-order conversations end-to-end using speech input and spoken responses.

It combines:
- **Speech-to-text** with Whisper
- **Chat completion** with Groq (`llama3-8b-8192`)
- **Text-to-speech** with OpenAI (`tts-1`)
- **Audio playback** with `pygame`

## Demo

- Video demo: [Chatbot Demo](https://drive.google.com/file/d/1CXmHUWSBI5t7EqEDJep4xU4XJYSLK_Sn/view?usp=sharing)

## Features

- Voice-based user input from microphone
- Persona-driven pizza ordering assistant prompt
- Conversation memory across turns in the same session
- Spoken assistant responses via generated `assistant.mp3`

## Project Structure

```text
myChatbot/
├── README.md
└── chatbot/
    ├── main.py
    ├── requirements.txt
    └── .gitignore
```

## Tech Stack

- Python 3.9+
- `groq` SDK for LLM chat responses
- `openai` SDK for text-to-speech
- `SpeechRecognition` + `whisper` + `soundfile` + `numpy` for transcription
- `pygame` for local audio playback
- `python-dotenv` for environment variables

## Prerequisites

- Python 3.9 or newer
- Working microphone
- API keys:
  - `GROQ_API_KEY`
  - `OPENAI_API_KEY`

## Setup

1. Clone the repository and go to the project:

   ```bash
   git clone <your-repo-url>
   cd myChatbot/chatbot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in `chatbot/`:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Run the Chatbot

From the `chatbot/` directory:

```bash
python main.py
```

Then speak into your microphone when prompted with `say something...`.

## How It Works

1. Captures audio from the microphone.
2. Converts speech to text with Whisper.
3. Sends the transcribed text to Groq chat completion.
4. Converts assistant response text to speech using OpenAI TTS.
5. Plays the generated response audio locally with `pygame`.

## Notes and Current Limitations

- The app currently loops forever until manually stopped (`Ctrl+C`).
- `assistant.mp3` is written on each response and not deleted automatically.
- The assistant is intentionally restricted to pizza-ordering conversations.
- First-time Whisper model loading can take longer and may require additional ML runtime dependencies.

## Troubleshooting

- **Microphone not detected**
  - Check OS microphone permissions and default input device.
- **No audio playback**
  - Confirm system audio output is working and `pygame` initialized correctly.
- **API/auth errors**
  - Verify `.env` keys are valid and loaded.
- **Whisper/ML dependency issues**
  - Ensure all requirements are installed in the active virtual environment.

## Future Improvements

- Add text-input fallback mode
- Add graceful exit command (for example: "quit")
- Delete temporary audio files after playback
- Add unit and integration tests
- Package as a CLI application

