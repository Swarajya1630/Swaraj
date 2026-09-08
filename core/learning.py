"""
Swaraj Learning System
=====================
Teaches users how Swaraj works.
Explains actual implementation details.
"""

import os
from core.logger import logger


class LearningSystem:
    def __init__(self):
        self.topics = self._build_topics()

    def _build_topics(self):
        return {
            "architecture": {
                "keywords": ["architecture", "structure", "design", "how are you built", "how do you work", "explain your code", "show me your modules"],
                "response": self._explain_architecture
            },
            "wake_word": {
                "keywords": ["wake word", "wake", "how do you hear me", "how do you activate", "how does listening work"],
                "response": self._explain_wake_word
            },
            "stt": {
                "keywords": ["speech to text", "stt", "how do you understand my voice", "how do you hear", "voice recognition"],
                "response": self._explain_stt
            },
            "tts": {
                "keywords": ["text to speech", "tts", "how do you speak", "how do you talk", "voice output"],
                "response": self._explain_tts
            },
            "ai": {
                "keywords": ["ai", "artificial intelligence", "how do you think", "how do you understand", "ollama", "mistral", "how do you call the ai"],
                "response": self._explain_ai
            },
            "commands": {
                "keywords": ["commands", "how do you open apps", "how do you execute", "command system", "how do you do things"],
                "response": self._explain_commands
            },
            "ui": {
                "keywords": ["ui", "interface", "floating widget", "rajmudra", "how does your ui work", "how does the界面 work"],
                "response": self._explain_ui
            },
            "startup": {
                "keywords": ["startup", "start with windows", "how do you start", "autostart", "boot"],
                "response": self._explain_startup
            },
            "sleep": {
                "keywords": ["sleep", "wake", "resume", "lid close", "hibernate", "how do you handle sleep"],
                "response": self._explain_sleep
            },
            "memory": {
                "keywords": ["memory", "remember", "how do you remember", "conversation history", "forget"],
                "response": self._explain_memory
            },
            "tray": {
                "keywords": ["tray", "system tray", "background", "minimize"],
                "response": self._explain_tray
            },
            "sound": {
                "keywords": ["sound", "audio", "beep", "chime", "feedback"],
                "response": self._explain_sound
            },
            "files": {
                "keywords": ["files", "code structure", "project structure", "folders"],
                "response": self._explain_files
            },
            "flow": {
                "keywords": ["what happens when", "flow", "pipeline", "lifecycle", "process"],
                "response": self._explain_flow
            },
            "debug": {
                "keywords": ["debug", "diagnostics", "health", "status", "check yourself"],
                "response": self._debug_self
            },
            "project_status": {
                "keywords": ["project status", "version", "what can you do", "features"],
                "response": self._project_status
            },
            "camera": {
                "keywords": ["camera", "webcam", "screenshot", "face detection", "qr code", "photo", "picture", "scan"],
                "response": self._explain_camera
            },
            "semantic_memory": {
                "keywords": ["semantic", "vector", "embedding", "similarity search", "memory search"],
                "response": self._explain_semantic_memory
            },
            "email_calendar": {
                "keywords": ["email", "calendar", "event", "meeting", "contact", "schedule", "appointment"],
                "response": self._explain_email_calendar
            },
            "wake_training": {
                "keywords": ["wake word training", "custom wake", "train wake", "activation phrase", "custom activation"],
                "response": self._explain_wake_training
            },
            "pyinstaller": {
                "keywords": ["exe", "executable", "build", "package", "distribute", "pyinstaller"],
                "response": self._explain_pyinstaller
            }
        }

    def check(self, text):
        """Check if text is a learning question."""
        text_lower = text.lower()

        for topic_key, topic in self.topics.items():
            for keyword in topic["keywords"]:
                if keyword in text_lower:
                    return topic["response"]()

        return None

    def _explain_architecture(self):
        return """SWARAJ ARCHITECTURE

I am built with a modular Python architecture:

FLOW:
Microphone -> Wake Word -> STT -> AI -> Commands -> TTS -> Speaker

LAYERS:
1. Desktop Layer - Main process, Windows integration
2. UI Layer - Floating widget, expanded window, Rajmudra
3. Voice Layer - Microphone, wake word, STT, TTS
4. AI Layer - Ollama (Mistral model), intent extraction
5. Command Layer - Router, handlers, safe execution
6. Memory Layer - Short-term, long-term, preferences

KEY FILES:
- app/main.py = Entry point and lifecycle
- core/router.py = Command routing
- core/pipeline.py = Speech pipeline
- ui/compact/widget.py = Floating Rajmudra widget
- commands/*.py = Command handlers

I use Python with tkinter for UI, Ollama for AI, and pyttsx3 for speech."""

    def _explain_wake_word(self):
        return """WAKE WORD SYSTEM

I listen for "Hey Swaraj" or "Swaraj" using:

FLOW:
Microphone -> Audio Capture -> Pattern Matching -> Activation

HOW IT WORKS:
1. Microphone captures audio continuously (low CPU)
2. Audio is checked against wake phrases
3. When detected, I enter LISTENING mode
4. Sound cue plays (ascending chime)

FILES:
- core/wake_word_local.py -> Wake word detector
- core/pipeline.py -> Manages the wake->listen cycle

TECHNOLOGY:
- SpeechRecognition library for audio processing
- Google Speech API for recognition (requires internet)
- Energy-based detection as fallback

When I hear my name, my Rajmudra widget illuminates and I start listening."""

    def _explain_stt(self):
        return """SPEECH-TO-TEXT (STT)

After wake word detection, I convert your speech to text:

FLOW:
Audio -> SpeechRecognition -> Google API -> Text

HOW IT WORKS:
1. Microphone captures your speech (5-10 seconds)
2. Audio is sent to Google Speech Recognition
3. Text is returned to me
4. I process the text as a command

FILES:
- listener.py -> SpeechRecognizer class
- core/pipeline.py -> Manages the listening cycle

TECHNOLOGY:
- SpeechRecognition library
- Google Speech Recognition API (free, requires internet)
- Supports English, Hindi, Marathi

I try recognition in all three languages until one succeeds."""

    def _explain_tts(self):
        return """TEXT-TO-SPEECH (TTS)

I speak responses using pyttsx3:

FLOW:
Response Text -> pyttsx3 Engine -> Speaker

HOW IT WORKS:
1. I generate a text response
2. pyttsx3 converts text to audio
3. Audio plays through your speakers

FILES:
- speaker.py -> Speaker class

TECHNOLOGY:
- pyttsx3 (offline, no internet needed)
- Uses Windows SAPI5 voice engine
- Supports multiple voices (English, Hindi)

I can adjust speech rate and volume from settings."""

    def _explain_ai(self):
        return """AI BRAIN (Ollama + Mistral)

I use a local AI model to understand you:

FLOW:
Your Text -> Ollama API -> Mistral Model -> Response

HOW IT WORKS:
1. Your text is sent to Ollama (running locally)
2. Mistral model processes the text
3. AI generates a response
4. Response is returned to you

FILES:
- ai_brain.py -> AIBrain class
- config/settings.py -> AI configuration

TECHNOLOGY:
- Ollama (local AI server)
- Mistral model (7B parameters)
- No cloud API needed (100% local)

CONFIGURATION:
- Model: mistral (configurable)
- Temperature: 0.8
- Max tokens: 200

The AI knows about you through the identity system."""

    def _explain_commands(self):
        return """COMMAND SYSTEM

I use a modular command router:

FLOW:
User Text -> Intent Detection -> Command Handler -> Response

HOW IT WORKS:
1. Your text is analyzed for patterns
2. Intent is detected (open app, search, etc.)
3. Appropriate handler executes the command
4. Response is generated

FILES:
- core/router.py -> CommandRouter
- commands/app_control.py -> Open/close apps
- commands/system_control.py -> Time, date, status
- commands/media_control.py -> Volume, playback
- commands/web_search.py -> Search, weather
- commands/productivity.py -> Reminders, notes

SAFE EXECUTION:
- Only approved commands are executed
- No arbitrary shell commands
- Allowlisted applications only

Example: "open Chrome" -> AppControlCommand -> subprocess.Popen("chrome.exe")"""

    def _explain_ui(self):
        return """USER INTERFACE

I have two UI modes:

COMPACT WIDGET:
- Small floating window (top-right)
- Rajmudra at center
- State indicator (idle/listening/thinking/speaking)
- Animated waveform
- Click to expand

EXPANDED WINDOW:
- Full assistant interface
- Large Rajmudra
- Conversation history
- Input field
- System status

FILES:
- ui/compact/widget.py -> CompactWidget
- ui/expanded/window.py -> ExpandedWindow
- ui/animations.py -> AnimationHelper
- assets/branding/rajmudra_*.png -> Rajmudra images

TECHNOLOGY:
- tkinter (Python GUI)
- Canvas-based drawing
- PIL/Pillow for images
- Frameless, always-on-top windows

The Rajmudra is the visual identity - it stays stable while animations happen around it."""

    def _explain_startup(self):
        return """WINDOWS STARTUP

I can start automatically with Windows:

FLOW:
Windows Login -> Registry Entry -> Swaraj Launches

HOW IT WORKS:
1. Registry key points to my executable
2. Windows runs me on login
3. I start in background mode
4. System tray icon appears

FILES:
- services/startup/startup_service.py -> StartupService

CONFIGURATION:
- Settings -> General -> "Start with Windows"
- Uses HKEY_CURRENT_USER registry

TECHNOLOGY:
- Windows Registry API
- Python winreg module

I register myself in: Software\\Microsoft\\Windows\\CurrentVersion\\Run"""

    def _explain_sleep(self):
        return """SLEEP/WAKE HANDLING

I gracefully handle Windows sleep:

FLOW:
Running -> Windows Sleep -> Pause -> Windows Wake -> Resume

HOW IT WORKS:
1. I detect Windows power state changes
2. On sleep: I pause microphone and processing
3. On wake: I reinitialize services
4. Wake word detection resumes

FILES:
- services/windows/power_handler.py -> PowerStateHandler

TECHNOLOGY:
- Windows Power Broadcasting (WM_POWERBROADCAST)
- Polling fallback if win32gui unavailable

I do NOT prevent Windows from sleeping.
I do NOT keep your laptop awake.
I recover automatically after wake."""

    def _explain_memory(self):
        return """MEMORY SYSTEM

I remember our conversations:

SHORT-TERM MEMORY:
- Last 100 conversations
- Current context
- Session data

LONG-TERM MEMORY:
- Facts about you
- Patterns learned
- Relationships

FILES:
- core/memory.py -> MemorySystem
- config/memory/short_term.json
- config/memory/long_term.json

HOW IT WORKS:
1. I save each conversation
2. I extract facts (name, age, city, etc.)
3. I remember your preferences
4. I use context for better responses

Example: You say "my name is Shiva"
I store: {"owner_name": "Shiva"}
Next time I know your name!"""

    def _explain_tray(self):
        return """SYSTEM TRAY

I run in the background with a tray icon:

FILES:
- ui/tray/system_tray.py -> SystemTray

MENU OPTIONS:
- Open Swaraj -> Shows floating widget
- Pause Listening -> Stops wake word detection
- Resume Listening -> Restarts wake word
- Settings -> Opens settings window
- Restart -> Restarts the application
- Exit -> Closes Swaraj

TECHNOLOGY:
- pystray library
- PIL/Pillow for icon
- Windows system tray API

The tray icon shows my state:
- Cyan = Listening
- Gray = Paused
- Purple = Thinking
- Green = Speaking"""

    def _explain_sound(self):
        return """SOUND FEEDBACK

I play audio cues for different states:

SOUNDS:
- Wake: Ascending chime (3 tones)
- Listening: Short beep
- Thinking: Medium tone
- Success: Two ascending tones
- Error: Descending tones

FILES:
- core/sound.py -> SoundFeedback

TECHNOLOGY:
- pyaudio for playback
- Programmatic tone generation (sine waves)
- No external audio files needed

FLOW:
State Change -> Generate Tone -> pyaudio -> Speaker

I can be muted from Settings -> Sound."""

    def _explain_files(self):
        return """PROJECT STRUCTURE

swaraj/
├── app/
│   └── main.py              # Entry point
├── config/
│   └── settings.py          # Configuration
├── core/
│   ├── logger.py            # Logging
│   ├── memory.py            # Memory system
│   ├── pipeline.py          # Speech pipeline
│   ├── router.py            # Command router
│   ├── sound.py             # Sound feedback
│   └── wake_word_local.py   # Wake word
├── commands/
│   ├── app_control.py       # App management
│   ├── media_control.py     # Volume, playback
│   ├── productivity.py      # Reminders, notes
│   ├── system_control.py    # Time, date, status
│   └── web_search.py        # Search, weather
├── ui/
│   ├── compact/widget.py    # Floating widget
│   ├── expanded/window.py   # Full interface
│   ├── settings/window.py   # Settings
│   └── tray/system_tray.py  # System tray
├── services/
│   ├── startup/             # Windows startup
│   └── windows/             # Power handling
└── assets/branding/         # Rajmudra images

KEY ENTRY POINT:
python app/main.py"""

    def _explain_flow(self):
        return """COMPLETE USER FLOW

When you use me, here's what happens:

1. DORMANT STATE
   - I'm listening for "Hey Swaraj"
   - Low CPU usage
   - Rajmudra widget visible

2. WAKE DETECTED
   - Sound cue plays
   - Widget shows LISTENING
   - Microphone activates

3. SPEECH CAPTURED
   - Audio sent to Google STT
   - Text returned
   - Widget shows THINKING

4. COMMAND PROCESSED
   - Router detects intent
   - Handler executes action
   - Response generated

5. RESPONSE SPOKEN
   - TTS speaks response
   - Widget shows SPEAKING

6. BACK TO DORMANT
   - After 3 seconds
   - Listening resumes

COMPLETE FLOW:
You -> "Hey Swaraj" -> Wake -> Listen -> STT -> AI/Commands -> TTS -> You hear response -> Dormant"""

    def _debug_self(self):
        """Debug system health."""
        issues = []

        # Check config
        try:
            from config.settings import Config
            Config()
        except Exception as e:
            issues.append(f"Config: {e}")

        # Check memory
        try:
            from core.memory import MemorySystem
            m = MemorySystem()
            stats = m.get_stats()
        except Exception as e:
            issues.append(f"Memory: {e}")

        # Check sound
        try:
            from core.sound import SoundFeedback
            s = SoundFeedback()
        except Exception as e:
            issues.append(f"Sound: {e}")

        # Check AI
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=3)
            if r.status_code != 200:
                issues.append("Ollama: Not responding")
        except:
            issues.append("Ollama: Not running (start with: ollama serve)")

        # Check microphone
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            if p.get_device_count() == 0:
                issues.append("Microphone: No devices found")
            p.terminate()
        except Exception as e:
            issues.append(f"Microphone: {e}")

        if issues:
            return "DIAGNOSTICS:\n" + "\n".join(f"- {i}" for i in issues)
        return "DIAGNOSTICS: All systems healthy!"

    def _project_status(self):
        return """SWARAJ PROJECT STATUS

VERSION: 1.0.0
NAME: SWARAJ - Smart Wide-purpose Automated Reasoning And Assistance Junction

IMPLEMENTED FEATURES:
✅ Configuration system
✅ Structured logging
✅ Windows startup registration
✅ System tray icon
✅ Sleep/resume handling
✅ Floating widget (Rajmudra)
✅ Expanded assistant window
✅ Local wake word detection
✅ Speech pipeline (wake->listen->process->respond)
✅ Command router with intent detection
✅ App control (open/close)
✅ System control (time, date, status)
✅ Media control (volume, playback)
✅ Web search (Google, YouTube, Wikipedia)
✅ Weather information
✅ Reminders and notes
✅ Enhanced memory system
✅ Settings UI
✅ Sound feedback
✅ Rajmudra visual identity

AI PROVIDER: Ollama (Mistral model)
VOICE: Google Speech API + pyttsx3
UI: tkinter (Python)
CAMERA: OpenCV (face detection, QR scanning)
MEMORY: TF-IDF semantic search
CALENDAR: Local event storage
BUILD: PyInstaller (Windows .exe)

ADDITIONAL FEATURES:
✅ Camera (screenshot, face detection, QR scanning)
✅ Semantic memory (vector search)
✅ Email/Calendar integration
✅ Custom wake word training
✅ PyInstaller packaging
✅ Learning/Tutorial system

START COMMAND: python app/main.py
TEXT MODE: python app/main.py --text
UI MODE: python app/main.py --ui
BUILD COMMAND: build.bat (creates dist/Swaraj/Swaraj.exe)"""

    def _explain_camera(self):
        return """CAMERA SYSTEM

I can use your webcam for various tasks:

CAPABILITIES:
• Take screenshots from webcam
• Detect faces using Haar cascades
• Scan QR codes
• Get camera info

FILES:
- core/camera.py -> CameraModule

TECHNOLOGY:
- OpenCV (cv2) for computer vision
- Haar cascade for face detection
- Built-in QRCodeDetector

SAY:
- "Take screenshot" - capture webcam image
- "Detect faces" - find faces in view
- "Scan QR" - read QR code
- "Camera info" - show camera details

Files saved to: swaraj/screenshots/

Face detection uses: haarcascade_frontalface_default.xml"""

    def _explain_semantic_memory(self):
        return """SEMANTIC MEMORY

I use vector search for context-aware memory:

HOW IT WORKS:
1. Text is converted to TF-IDF vectors
2. Stored with metadata
3. Searched using cosine similarity
4. Provides context for AI responses

FILES:
- core/semantic_memory.py -> SemanticMemory
- config/memory/vectors.json

TECHNOLOGY:
- TF-IDF (Term Frequency-Inverse Document Frequency)
- Cosine similarity for matching
- Local storage (no external DB)

FEATURES:
• Auto-learns from conversations
• Semantic search (meaning-based)
• Context injection for AI
• Vocabulary management

STATS:
- Entries: text chunks stored
- Vocabulary: unique words indexed"""

    def _explain_email_calendar(self):
        return """EMAIL/CALENDAR INTEGRATION

I manage events and contacts locally:

EVENTS:
• Add events with date/time
• List events by date
• View upcoming events (7 days)
• Delete events

CONTACTS:
• Add contacts (name, email, phone)
• Search contacts by name
• Local storage

FILES:
- core/email_calendar.py -> EmailCalendarModule
- config/calendar/events.json
- config/calendar/contacts.json

SAY:
- "Add event meeting on 2024-01-15 at 10:00"
- "List events" or "Show calendar"
- "Upcoming events" or "What's next"
- "Add contact John with email john@example.com"
- "Find contact John"

Supports: YYYY-MM-DD and DD/MM/YYYY formats"""

    def _explain_wake_training(self):
        return """CUSTOM WAKE WORD TRAINING

I can learn custom activation phrases:

CAPABILITIES:
• Record wake word samples
• Add custom phrases
• Remove phrases
• Enable/disable phrases

FILES:
- core/wake_word_train.py -> WakeWordTrainer
- config/wake_words/custom_words.json
- config/wake_words/recordings/

DEFAULT WAKE WORDS:
- "Hey Swaraj"
- "Swaraj"

CUSTOM PHRASES:
- Added via training
- Stored as text patterns
- Detected alongside defaults

SAY:
- "Add wake word hello assistant"
- "List wake words"
- "Remove wake word hello assistant"

Recordings saved as WAV files for future reference."""

    def _explain_pyinstaller(self):
        return """PYINSTALLER PACKAGING

I can be packaged as a Windows executable:

BUILD PROCESS:
1. Run: build.bat
2. PyInstaller analyzes dependencies
3. Creates dist/Swaraj/ folder
4. Executable: dist/Swaraj/Swaraj.exe

FILES:
- Swaraj.spec -> PyInstaller configuration
- build.bat -> Build script

WHAT'S INCLUDED:
- All Python modules
- Assets (Rajmudra images)
- Config files
- All dependencies

DISTRIBUTION:
- Copy entire dist/Swaraj/ folder
- No Python required on target
- Runs on any Windows 10+ machine

COMMANDS:
- Build: build.bat
- Clean: pyinstaller --clean Swaraj.spec
- Debug: pyinstaller Swaraj.spec --debug

Output size: ~50-100MB"""
