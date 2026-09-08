# SWARAJ — Windows AI Voice Assistant

Your personal AI assistant powered by Ollama (100% local). Only YOU can talk to it.

Inspired by Chhatrapati Shivaji Maharaj's Rajmudra.

---

## Features

- **Rajmudra Visual Identity** — Golden seal as the core visual element
- **Floating Widget** — Top-right corner, always on top
- **Wake Word Detection** — "Hey Swaraj" or "Swaraj"
- **Voice Commands** — Open apps, search web, check weather, reminders
- **System Tray** — Runs in background
- **Windows Startup** — Launches automatically
- **Sleep/Resume Handling** — Recovers after Windows sleep
- **Multilingual** — English, Hindi, Marathi
- **Local AI** — Uses Ollama (no cloud API needed)
- **Settings UI** — Configure everything from the UI
- **Sound Feedback** — Audio cues for states

---

## Quick Start

### Prerequisites

1. **Python 3.10+** — [Download](https://python.org)
2. **Ollama** — [Download](https://ollama.com)
3. **Mistral Model** — Run: `ollama pull mistral`

### Installation

```bash
# Clone the repository
git clone https://github.com/Swarajya1630/Swaraj.git
cd Swaraj

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
# Background mode (recommended)
python app/main.py

# Text mode
python app/main.py --text

# UI mode
python app/main.py --ui
```

Or double-click `start.bat`.

---

## Voice Commands

| Command | Action |
|---------|--------|
| "Hey Swaraj" | Wake up |
| "open Chrome" | Opens Chrome |
| "open my project" | Opens project folder |
| "what time is it" | Tells time |
| "what's the weather" | Shows weather |
| "volume up" | Increases volume |
| "play lofi on Spotify" | Opens Spotify search |
| "search Google for Python" | Opens Google |
| "remind me to drink water in 30 min" | Sets reminder |
| "note buy groceries" | Saves note |
| "system status" | Shows CPU/RAM/Disk |

---

## Project Structure

```
swaraj/
├── app/main.py              # Entry point
├── config/settings.py       # Configuration
├── core/                    # Core modules
│   ├── logger.py           # Logging
│   ├── memory.py           # Memory system
│   ├── pipeline.py         # Speech pipeline
│   ├── router.py           # Command router
│   ├── sound.py            # Sound feedback
│   └── wake_word_local.py  # Wake word
├── commands/                # Command handlers
│   ├── app_control.py      # App management
│   ├── media_control.py    # Volume, playback
│   ├── productivity.py     # Reminders, notes
│   ├── system_control.py   # Time, date, status
│   └── web_search.py       # Search, weather
├── ui/                      # User interface
│   ├── compact/widget.py   # Floating widget
│   ├── expanded/window.py  # Full interface
│   ├── settings/window.py  # Settings
│   └── tray/system_tray.py # System tray
├── services/                # Windows integration
│   ├── startup/            # Windows startup
│   └── windows/            # Power handling
└── assets/branding/         # Rajmudra assets
```

---

## Configuration

Settings are stored in `config/settings.json`.

Key settings:
- `general.start_with_windows` — Auto-launch with Windows
- `general.start_minimized` — Start to system tray
- `voice.wake_word_enabled` — Enable wake word detection
- `ai.model` — Ollama model (default: mistral)

---

## Architecture

```
Microphone
    ↓
Wake Word Detection ("Hey Swaraj")
    ↓
Speech-to-Text (Google API)
    ↓
Command Router (Intent Detection)
    ↓
Command Handler (App/System/Media/Web/Productivity)
    ↓
Response
    ↓
Text-to-Speech (pyttsx3)
    ↓
Return to Dormant
```

---

## Technologies

- **Python 3.10+**
- **Ollama** — Local AI (Mistral model)
- **tkinter** — GUI framework
- **SpeechRecognition** — Speech-to-text
- **pyttsx3** — Text-to-speech
- **pyaudio** — Microphone access
- **pystray** — System tray
- **Pillow** — Image handling
- **psutil** — System monitoring

---

## License

Personal project by Swayam Naik.

---

## Acknowledgments

- Chhatrapati Shivaji Maharaj — Inspiration for the Rajmudra identity
- Ollama — Local AI backend
- The open-source Python community
