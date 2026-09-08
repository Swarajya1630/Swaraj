"""
Camera Module
=============
OpenCV-based camera features for Swaraj.
Screenshot, face detection, QR scanning.
"""

import os
import threading
from datetime import datetime
from core.logger import logger

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    logger.warning("OpenCV not installed. Camera features unavailable.")


class CameraModule:
    def __init__(self):
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self._face_cascade = None
        self._qr_detector = None

    def _init_face_detector(self):
        if self._face_cascade is None and HAS_OPENCV:
            try:
                cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                self._face_cascade = cv2.CascadeClassifier(cascade_path)
            except Exception as e:
                logger.error(f"Face detector init failed: {e}")

    def _init_qr_detector(self):
        if self._qr_detector is None and HAS_OPENCV:
            try:
                self._qr_detector = cv2.QRCodeDetector()
            except Exception as e:
                logger.error(f"QR detector init failed: {e}")

    def is_available(self):
        return HAS_OPENCV

    def take_screenshot(self):
        """Capture screenshot from webcam."""
        if not HAS_OPENCV:
            return None, "OpenCV not installed. Run: pip install opencv-python"

        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None, "Could not open webcam"

            ret, frame = cap.read()
            cap.release()

            if not ret:
                return None, "Could not capture frame"

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            cv2.imwrite(filepath, frame)

            return filepath, f"Screenshot saved: {filename}"

        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None, f"Screenshot failed: {str(e)}"

    def detect_faces(self):
        """Detect faces in webcam feed."""
        if not HAS_OPENCV:
            return None, "OpenCV not installed"

        self._init_face_detector()
        if self._face_cascade is None:
            return None, "Face detector not available"

        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None, "Could not open webcam"

            ret, frame = cap.read()
            cap.release()

            if not ret:
                return None, "Could not capture frame"

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self._face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"faces_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            cv2.imwrite(filepath, frame)

            count = len(faces)
            return filepath, f"Detected {count} face(s). Saved: {filename}"

        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            return None, f"Face detection failed: {str(e)}"

    def scan_qr(self):
        """Scan QR code from webcam."""
        if not HAS_OPENCV:
            return None, "OpenCV not installed"

        self._init_qr_detector()
        if self._qr_detector is None:
            return None, "QR detector not available"

        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None, "Could not open webcam"

            for _ in range(30):
                ret, frame = cap.read()
                if not ret:
                    continue

                data, bbox, _ = self._qr_detector.detectAndDecode(frame)
                if data:
                    cap.release()
                    return data, f"QR Code: {data}"

            cap.release()
            return None, "No QR code detected"

        except Exception as e:
            logger.error(f"QR scan failed: {e}")
            return None, f"QR scan failed: {str(e)}"

    def get_camera_info(self):
        """Get available camera information."""
        if not HAS_OPENCV:
            return "OpenCV not installed"

        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                cap.release()
                return f"Camera: {width}x{height} @ {fps}fps"
            else:
                return "No camera detected"
        except Exception as e:
            return f"Camera error: {str(e)}"
