import subprocess
import time
import threading
import state
import os
import speech_recognition as sr
from intent_engine import detect_intent
from actions import execute
from face_engine import start_face

os.environ["DISPLAY"] = ":0"

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.3
recognizer.energy_threshold = 250
recognizer.dynamic_energy_threshold = False

def listen_once():

    # Wait only while robot is speaking
    while state.is_speaking:
        time.sleep(0.05)

    print("🎤 Listening...")

    try:
        process = subprocess.Popen(
            [
                "pw-cat", "--record", "-",
                "--format=s16",
                "--rate=16000",
                "--channels=1"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        # Reduced from 6 sec → 2 sec
        audio_data = process.stdout.read(16000 * 2 * 2)

        process.kill()

        if len(audio_data) == 0:
            return ""

        # Safety check
        if state.is_speaking:
            print("🔇 Discarding — robot is speaking")
            return ""

        audio = sr.AudioData(audio_data, 16000, 2)

        text = recognizer.recognize_google(audio)

        print(f"You said: {text}")

        return text.lower().strip()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError as e:
        print(f"❌ Google STT Error: {e}")
        return ""

    except Exception as e:
        print(f"❌ Error: {e}")
        return ""

def voice_loop():
    print("🎤 Voice Assistant Started...")

    while True:
        text = listen_once()

        if text == "" or state.is_speaking:
            continue

        intent = detect_intent(text)
        print(f"Intent: {intent}")

        execute(intent, text)

        # Hard wait after any command finishes
        while state.is_speaking:
            time.sleep(0.1)

        time.sleep(1.5)


if __name__ == "__main__":
    threading.Thread(target=voice_loop, daemon=True).start()
    start_face()