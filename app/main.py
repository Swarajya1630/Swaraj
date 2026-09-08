"""
Application Lifecycle
====================
Main entry point and lifecycle manager.
Handles initialization, running, and shutdown.
"""

import sys
import os
import signal
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from core.logger import logger


class JarvisApp:
    def __init__(self):
        self.config = Config()
        self._running = False
        self._shutdown_event = threading.Event()

        self.tray = None
        self.startup_service = None
        self.power_handler = None
        self.ui_compact = None
        self.ui_expanded = None

        self.ai_brain = None
        self.wake_detector = None
        self.speech_recognizer = None
        self.speaker = None
        self.identity = None

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info(f"Signal {signum} received, shutting down...")
        self.shutdown()

    def initialize(self):
        logger.startup("=== JARVIS Starting ===")
        logger.startup(f"Python: {sys.version}")
        logger.startup(f"Working dir: {os.getcwd()}")

        self._init_identity()
        self._init_ai()
        self._init_voice()
        self._init_services()

        logger.startup("=== JARVIS Initialized ===")
        return True

    def _init_identity(self):
        try:
            from identity import PersonalIdentity
            self.identity = PersonalIdentity()
            owner = self.identity.get_owner_name() or "Shiva"
            logger.startup(f"Identity loaded. Owner: {owner}")
        except Exception as e:
            logger.error(f"Identity init failed: {e}")

    def _init_ai(self):
        try:
            from ai_brain import AIBrain
            model = self.config.get("ai", "model", "mistral")
            self.ai_brain = AIBrain(model=model)
            logger.startup(f"AI Brain connected: {model}")
        except Exception as e:
            logger.warning(f"AI Brain offline: {e}")

    def _init_voice(self):
        try:
            from listener import SpeechRecognizer
            from speaker import Speaker
            from wake_word import WakeWordDetector

            self.speech_recognizer = SpeechRecognizer()
            self.speaker = Speaker(
                rate=self.config.get("voice", "speech_rate", 175),
                volume=self.config.get("voice", "volume", 0.9)
            )
            self.wake_detector = WakeWordDetector()
            logger.startup("Voice services initialized")
        except Exception as e:
            logger.error(f"Voice init failed: {e}")

    def _init_services(self):
        try:
            from services.startup.startup_service import StartupService
            self.startup_service = StartupService()

            if self.config.get("general", "start_with_windows"):
                if not self.startup_service.is_enabled():
                    self.startup_service.enable()
        except Exception as e:
            logger.error(f"Startup service init failed: {e}")

        try:
            from services.windows.power_handler import PowerStateHandler
            self.power_handler = PowerStateHandler()
            self.power_handler.register_callbacks(
                on_resume=self._on_resume,
                on_sleep=self._on_sleep
            )
            self.power_handler.start_listening()
        except Exception as e:
            logger.error(f"Power handler init failed: {e}")

    def _on_resume(self):
        logger.info("System resumed - reinitializing services")
        try:
            self._init_voice()
        except Exception as e:
            logger.error(f"Resume reinit failed: {e}")

    def _on_sleep(self):
        logger.info("System entering sleep - pausing services")

    def start_tray(self):
        try:
            from ui.tray.system_tray import SystemTray
            self.tray = SystemTray()
            self.tray.set_callbacks(
                open=self._on_tray_open,
                pause=self._on_tray_pause,
                resume=self._on_tray_resume,
                exit=self._on_tray_exit
            )
            self.tray.start()
        except Exception as e:
            logger.error(f"Tray init failed: {e}")

    def _on_tray_open(self):
        logger.info("Tray: Open assistant")
        self.show_compact_ui()

    def _on_tray_pause(self):
        logger.info("Tray: Pause listening")
        if self.tray:
            self.tray.update_status("paused")

    def _on_tray_resume(self):
        logger.info("Tray: Resume listening")
        if self.tray:
            self.tray.update_status("running")

    def _on_tray_exit(self):
        logger.info("Tray: Exit requested")
        self.shutdown()

    def show_compact_ui(self):
        if self.ui_compact is None:
            try:
                from ui.compact.widget import CompactWidget
                self.ui_compact = CompactWidget(self)
                self.ui_compact.start()
            except Exception as e:
                logger.error(f"Compact UI failed: {e}")

    def run(self, mode="background"):
        self._running = True
        logger.startup(f"Running in {mode} mode")

        if mode == "background":
            self.start_tray()
            if self.config.get("general", "start_minimized"):
                logger.startup("Starting minimized to tray")
            else:
                self.show_compact_ui()

            self._wait_for_shutdown()

        elif mode == "text":
            self._run_text_mode()

        elif mode == "ui":
            self.show_compact_ui()
            self._wait_for_shutdown()

    def _wait_for_shutdown(self):
        while self._running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.shutdown()
                break

    def _run_text_mode(self):
        owner = self.identity.get_owner_name() if self.identity else "Shiva"
        print(f"\nHey {owner}! SWARAJ online. Type 'exit' to quit.\n")

        while self._running:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("See you later!")
                    self.shutdown()
                    break

                response, lang = self._process_command(user_input)
                print(f"Swaraj: {response}\n")

            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Text mode error: {e}")

    def _process_command(self, text):
        from task_automation import TaskAutomation
        automation = TaskAutomation()

        task_result = automation.execute_command(text, self.config.get("general", "language", "english"))
        if task_result:
            return task_result, self.config.get("general", "language", "english")

        if self.ai_brain:
            return self.ai_brain.think(text)

        return "AI is offline. I can still open apps and search the web.", "english"

    def shutdown(self):
        if not self._running:
            return

        logger.startup("=== JARVIS Shutting Down ===")
        self._running = False

        if self.tray:
            self.tray.stop()

        if self.power_handler:
            self.power_handler.stop()

        if self.ui_compact:
            try:
                self.ui_compact.stop()
            except:
                pass

        self._shutdown_event.set()
        logger.startup("=== JARVIS Stopped ===")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Swaraj AI Assistant")
    parser.add_argument("--text", action="store_true", help="Text mode")
    parser.add_argument("--ui", action="store_true", help="UI mode")
    parser.add_argument("--setup", action="store_true", help="Setup mode")
    parser.add_argument("--startup", action="store_true", help="Started by Windows")
    parser.add_argument("--lang", type=str, default="english", help="Language")
    args = parser.parse_args()

    app = JarvisApp()

    if not app.initialize():
        logger.error("Initialization failed!")
        sys.exit(1)

    if args.setup:
        app._run_text_mode()
    elif args.text:
        app.run(mode="text")
    elif args.ui:
        app.run(mode="ui")
    else:
        app.run(mode="background")


if __name__ == "__main__":
    main()
