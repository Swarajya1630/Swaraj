# SWARAJ

**S**mart **W**ide-purpose **A**utomated **R**easoning **A**nd assistance **J**unction

Your personal AI best friend that runs 100% locally on your laptop. No API keys, no internet needed for AI. Supports English, Hindi, and Marathi.

---

## Features

- **100% Free & Local** - Uses Ollama for AI, no API costs
- **Multilingual** - English, Hindi, Marathi
- **Personal Friend** - Only YOU can talk to it
- **Website Bookmarks** - Save and open links with custom names
- **App Launcher** - Open any app with voice/text
- **Jarvis-style UI** - Rajmudra startup, arc reactor interface
- **Voice Commands** - Say "Hey Swaraj" to activate

---

## Quick Start

### 1. Install Ollama
Download from [ollama.com](https://ollama.com)

```bash
ollama serve
ollama pull mistral
```

### 2. Install Python Dependencies
```bash
pip install SpeechRecognition pyttsx3 python-dotenv requests wikipedia pyaudio Pillow
```

### 3. Setup (First Time)
```bash
python swaraj.py --setup
```

### 4. Run
```bash
python swaraj.py --text     # Text mode
python swaraj.py --ui       # GUI mode
python swaraj.py            # Voice mode
```

Or double-click `start.bat` for a menu.

---

## Commands

| Command | Description |
|---------|-------------|
| `open chrome` | Open Chrome browser |
| `search for AI` | Google search |
| `what time is it` | Tell current time |
| `save website youtube.com as youtube` | Save bookmark |
| `open youtube` | Open saved bookmark |
| `list websites` | Show all bookmarks |
| `switch to hindi` | Change language |
| `friendship stats` | Show friendship level |
| `exit` | Quit Swaraj |

---

## Project Structure

```
jarvis/
  swaraj.py          # Main entry point
  ai_brain.py        # Ollama AI integration
  listener.py        # Speech recognition
  speaker.py         # Text-to-speech
  task_automation.py # App launcher, web search
  wake_word.py       # "Hey Swaraj" detection
  identity.py        # Personal identity & memories
  ui.py              # Jarvis-style GUI
  assets/            # Images (Rajmudra)
  start.bat          # Quick launcher
```

---

## Tech Stack

- **Python 3.13+**
- **Ollama** - Local AI (Mistral model)
- **SpeechRecognition** - Voice to text
- **pyttsx3** - Text to voice
- **tkinter** - GUI framework
- **Pillow** - Image handling

---

## License

Personal project - Not for commercial use.

---

*Built with pride by Swayam*
