import subprocess
import os
import time
import state

PIPER_DIR = "/home/anirban06/robot/piper/piper"

def speak(text):
    try:
        state.is_speaking = True

        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = PIPER_DIR

        tts = subprocess.Popen(
            [
                f"{PIPER_DIR}/piper",
                "--model", "/home/anirban06/robot/piper/en_US-lessac-medium.onnx",
                "--output_file", "/tmp/speech.wav"
            ],
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env
        )
        tts.communicate(input=text.encode())

        # Play and wait for full completion
        subprocess.run(["pw-play", "/tmp/speech.wav"])

    except Exception as e:
        print(f"TTS Error: {e}")

    finally:
        time.sleep(0.7)           # Wait for speaker to fully stop
        state.is_speaking = False  # Only THEN open mic