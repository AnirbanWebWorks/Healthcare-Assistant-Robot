import serial
import time

# change this if needed
PORT = '/dev/ttyUSB0'

ser = serial.Serial(PORT, 9600, timeout=1)
time.sleep(2)   # allow Nano to reset

def send_command(cmd):
    ser.write((cmd + "\n").encode())
    print("Sent:", cmd)

# ===== TEST =====
send_command("HELLO")
time.sleep(3)

send_command("THANKYOU")
time.sleep(3)

send_command("HANDSHAKE")