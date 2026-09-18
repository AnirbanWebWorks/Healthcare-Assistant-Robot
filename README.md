# ORIX — AI-Powered Healthcare Assistant Robot

An AI-driven hospital assistant robot providing voice interaction, contactless vital-sign monitoring, and autonomous mobility for smart healthcare environments.

**Author:** Anirban Saha
**Guide:** Mrs. Sanghamitra Layek, Assistant Professor, Dept. of ECS
**Institute:** Narula Institute of Technology, Kolkata (MAKAUT)
**Degree:** B.Tech, Electronics & Instrumentation Engineering — June 2026

---

## Overview

ORIX assists patients, visitors, doctors, and hospital staff through:
- Natural voice interaction (speech-to-text → intent recognition → text-to-speech)
- Contactless heart-rate and SpO2 estimation via webcam-based Remote Photoplethysmography (rPPG)
- Hospital navigation guidance (ICU, OPD, reception, pharmacy, washroom, emergency ward)
- Wheel-based autonomous/semi-autonomous movement
- Emergency detection and alerting
- Animated on-screen face for Human-Robot Interaction (HRI)

## System Architecture

| Layer | Component | Role |
|---|---|---|
| High-level AI processing | Raspberry Pi 5 | Speech recognition, intent processing, rPPG, TTS, face animation |
| Low-level control | Arduino Nano | Motor direction, speed, wheel actuation |
| Link between Pi and Nano | HC-05 Bluetooth module (UART/SPP) | Wireless command transmission |
| Motor driver | BTS7960B | Bidirectional PWM motor control |
| Locomotion | 2x DC geared motors, differential drive | Forward/backward/turn |
| Vision | USB webcam | Face detection + rPPG signal extraction |
| Display | 5-inch LCD | Animated face, BPM/SpO2, alerts |
| Audio | Microphone + Bluetooth speaker | Voice input/output |
| Power | 2200 mAh LiPo + Power Distribution Board | Portable power delivery |

```
Mic → Google STT → Intent Engine → Action Dispatcher ─┬─→ TTS (Piper) → Bluetooth Speaker
                                                        ├─→ Bluetooth (HC-05) → Arduino Nano → Motor Driver → Wheels
                                                        ├─→ rPPG (webcam) → BPM/SpO2
                                                        └─→ Face Engine (Tkinter) → LCD
```

## Software Modules

| File | Responsibility |
|---|---|
| `voice_main.py` | Main loop: records short audio clips (`pw-cat`), sends to Google STT, routes text to the intent engine, launches the face UI on the main thread |
| `intent_engine.py` | Keyword-based intent classification (`detect_intent`) with a defined-but-unused spaCy similarity fallback (`similarity_match`) for future NLP-based matching |
| `actions.py` | Executes the action tied to each detected intent — speech, face expression, motor commands, SpO2/BPM check trigger, emergency alert |
| `face_engine.py` | Fullscreen Tkinter canvas rendering the robot's animated face (idle, smile, talk, blink) |
| `spo2_cam.py` | Haar-cascade face detection → forehead ROI → green-channel signal → Butterworth bandpass filter → peak detection for **BPM**; see *Known Limitations* for SpO2 |
| `nano_control.py` | Standalone serial test script for sending basic commands to the Nano |
| `tts.py` | Wraps the Piper TTS engine, synthesizes speech to a WAV file, plays it via `pw-play` |
| `state.py` | Single shared flag (`is_speaking`) used to gate the microphone while the robot is talking |
| `haarcascade_frontalface_default.xml` | OpenCV pretrained Haar cascade used for facial ROI detection |

## Hardware Components

- Raspberry Pi 5 (main processing unit)
- Arduino Nano (motor/actuator controller)
- HC-05 Bluetooth module + USB Bluetooth dongle
- USB webcam
- 5-inch LCD display
- Bluetooth speaker
- Microphone
- BTS7960B motor driver
- 2x DC geared motors
- Power Distribution Board (PDB)
- 2200 mAh LiPo battery
- Wheel-based chassis

## Setup

**Dependencies (Raspberry Pi, Python 3):**
```bash
pip install pyserial opencv-python numpy scipy SpeechRecognition spacy --break-system-packages
python -m spacy download en_core_web_md
```

**Also required on the Pi:**
- Piper TTS binary + an `en_US-lessac-medium.onnx` voice model (path set in `tts.py`)
- PipeWire audio tools (`pw-cat`, `pw-play`)
- Bluetooth paired and bound to `/dev/rfcomm0` for the Nano link:
  ```bash
  sudo rfcomm bind /dev/rfcomm0 <HC-05_MAC_ADDRESS> 1
  ```
- Arduino Nano flashed with firmware that accepts `F`, `B`, `L`, `R`, `S`/`STOP` and the named event commands (`HELLO`, `THANKYOU`, `WAVE_START`, `EXPLAIN_START`, `EXPLAIN_STOP`)

**Run:**
```bash
python voice_main.py
```
This starts the voice-recognition loop on a background thread and the face UI on the main thread.

## Known Limitations

- **SpO2 is currently simulated** — `spo2_cam.py` returns `random.randint(98, 100)` rather than computing it from the red/green AC-DC ratio described in the project report. BPM is genuinely computed from the rPPG signal; SpO2 is a placeholder pending calibration.
- `intent_engine.py`'s spaCy similarity fallback (`similarity_match`) is defined but never called — `detect_intent()` relies entirely on keyword matching.
- `nano_control.py` targets `/dev/ttyUSB0` while the live pipeline (`actions.py`) uses `/dev/rfcomm0` — this file is a standalone test script, not part of the runtime path.
- Navigation is scripted/verbal (fixed directional answers) rather than SLAM-based; no autonomous path planning is implemented yet.

## Future Scope

- Autonomous navigation via SLAM (LiDAR/depth camera + obstacle avoidance)
- Real SpO2 estimation using the AC/DC red-green ratio, with calibration against a reference pulse oximeter
- Additional biomedical sensors (ECG, temperature, blood pressure, respiration)
- ML-based intent classification (activating/replacing the current spaCy fallback)
- Face recognition and patient identification
- Cloud/IoT connectivity for remote monitoring and hospital dashboard integration
- SMS/network-based emergency alerting to staff

## Results Summary (from experimental testing)

- Voice commands (movement, BPM/SpO2 check, navigation queries, "help") were correctly recognized and executed with minimal delay.
- Bluetooth link between Pi and Nano was stable with low communication delay.
- BPM tracking stayed close to reference values under stable lighting across 100 test samples; accuracy degraded with poor lighting/motion.
