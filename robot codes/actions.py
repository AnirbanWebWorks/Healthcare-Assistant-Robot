import serial
import time
import datetime
import threading
import requests
import state
from tts import speak
from face_engine import set_expression
from spo2_cam import measure_spo2
import os

# ================= BLUETOOTH SERIAL SETUP =================
PORT = '/dev/rfcomm0'   # Bluetooth via HC-05
ser = None


def get_serial():
    try:
        s = serial.Serial(PORT, 9600, timeout=1)
        time.sleep(1)
        print("Bluetooth Serial Connected to Nano!")
        return s
    except Exception as e:
        print(f"Serial connect failed: {e}")
        return None

get_serial()

def send_command(cmd):
    global ser
    try:
        if ser is None or not ser.is_open:
            print("Reconnecting serial...")
            ser = get_serial()
        if ser:
            ser.write((cmd + "\n").encode())
            print("Sent:", cmd)
    except Exception as e:
        print(f"Serial Error: {e}")
        ser = None   # Force reconnect next time

def move(direction, seconds=3):
    send_command(direction)
    print(f"Moving {direction} for {seconds} seconds...")
    time.sleep(seconds)
    send_command("STOP")
    print("Stopped!")


# ================= EXECUTE FUNCTION =================
def execute(intent, text):

    # ---------- EMERGENCY ----------
    if intent == "emergency":
        set_expression("talk")
        send_command("WAVE_START")
        response = "Emergency detected. Alerting medical staff immediately."
        set_expression("idle")
        state.is_speaking = True
        speak(response)
        time.sleep(1)
        state.is_speaking = False

    # ---------- SPO2 ----------
    elif intent == "spo2_check":

        set_expression("talk")

        send_command("EXPLAIN_START")

        state.is_speaking = True

        speak(
            "Please stay still. "
            "Checking oxygen level and heart rate for 10 seconds."
        )

        state.is_speaking = False

        bpm, spo2, status, confidence = measure_spo2()

        if bpm == 0 or spo2 == 0:

            response = (
                "Sorry. "
                "I could not get a reliable reading. "
                "Please try again."
            )

        else:

            response = (
                f"Average heart rate is {bpm} beats per minute. "
                f"Average oxygen level is {spo2} percent. "
                f"Status is {status}."
            )

        set_expression("happy")

        state.is_speaking = True

        speak(response)

        time.sleep(1)

        state.is_speaking = False

        send_command("EXPLAIN_STOP")

        set_expression("idle")

    # ---------- THANK YOU ----------
    elif intent == "thanks":
        set_expression("talk")
        state.is_speaking = True
        threading.Thread(target=speak, args=("You're welcome. I am always here to help.",)).start()
        send_command("THANKYOU")
        set_expression("idle")
        state.is_speaking = False

    elif intent == "icu_navigation":

        set_expression("talk")

        speak("The ICU is on the left side.")

        set_expression("idle")

    elif intent == "emergency_navigation":

        set_expression("talk")

        speak("The emergency ward is straight ahead.")

        set_expression("idle")

    elif intent == "opd_navigation":

        set_expression("talk")

        speak("The O P D is on the second floor.")

        set_expression("idle")

    elif intent == "reception_navigation":

        set_expression("talk")

        speak("The reception is near the main entrance.")

        set_expression("idle")

    elif intent == "pharmacy_navigation":

        set_expression("talk")

        speak("The pharmacy is beside the reception.")

        set_expression("idle")

    elif intent == "washroom_navigation":

        set_expression("talk")

        speak("The washroom is on the right side.")

        set_expression("idle")

    # ---------- MOVE FORWARD ----------
    elif intent == "move_forward" or intent == "forward":
        set_expression("talk")
        speak("Moving forward.")
        move("F", seconds=3)
        set_expression("idle")

    # ---------- MOVE BACKWARD ----------
    elif intent == "move_backward":
        set_expression("talk")
        speak("Moving backward.")
        move("B", seconds=3)
        set_expression("idle")

    # ---------- TURN LEFT ----------
    elif intent == "move_left":
        set_expression("talk")
        speak("Turning left.")
        move("L", seconds=3)
        set_expression("idle")

    # ---------- TURN RIGHT ----------
    elif intent == "move_right":
        set_expression("talk")
        speak("Turning right.")
        move("R", seconds=3)
        set_expression("idle")

    # ---------- STOP ----------
    elif intent == "move_stop":
        set_expression("talk")
        send_command("S")
        speak("Stopping.")
        set_expression("idle")

    # ---------- TIME ----------
    elif intent == "time_query":
        set_expression("talk")
        now = datetime.datetime.now().strftime("%H:%M")
        send_command("EXPLAIN_START")
        response = f"The time is {now}"
        state.is_speaking = True
        speak(response)
        time.sleep(1)
        state.is_speaking = False
        send_command("EXPLAIN_STOP")
        set_expression("idle")

    # ---------- GREETING ----------
    elif intent == "greeting":
        set_expression("smile")
        threading.Thread(target=speak, args=("Hello, I am Orix. How can I assist you?",)).start()
        send_command("HELLO")
        set_expression("idle")

    # ---------- EXIT ----------
    elif intent == "exit":
        set_expression("talk")
        send_command("S")
        response = "Shutting down. Goodbye."
        state.is_speaking = True
        speak(response)
        time.sleep(1)
        state.is_speaking = False
        set_expression("idle")
        exit()

    # ---------- DEFAULT ----------
    else:
        set_expression("idle")
    

    return