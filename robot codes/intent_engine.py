import spacy

nlp = spacy.load("en_core_web_md")

# 🔥 EXPANDED INTENT DATABASE

INTENTS = {

    # ─────────────────────────────
    # EMERGENCY
    # ─────────────────────────────

    "emergency": [
        "help",
        "emergency",
        "call doctor",
        "urgent",
        "critical",
        "save me",
        "need help",
        "doctor please",
        "call nurse",
        "i need assistance",
        "patient emergency"
    ],


    # ─────────────────────────────
    # GREETINGS
    # ─────────────────────────────

    "greeting": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "hello robot",
        "hello orix"
    ],


    # ─────────────────────────────
    # THANKS
    # ─────────────────────────────

    "thanks": [
        "thank you",
        "thanks",
        "thanks a lot",
        "thank you so much",
        "appreciate it",
        "thanks orix",
        "great job",
        "nice work"
    ],


    # ─────────────────────────────
    # TIME QUERY
    # ─────────────────────────────

    "time_query": [
        "time",
        "current time",
        "what time",
        "tell me the time",
        "what is the time now"
    ],


    # ─────────────────────────────
    # DOCTOR INFO
    # ─────────────────────────────

    "doctor_info": [
        "doctor",
        "doctor available",
        "is doctor available",
        "where is doctor",
        "doctor room",
        "call doctor",
        "doctor timing",
        "doctor available now"
    ],


    # ─────────────────────────────
    # GENERAL NAVIGATION
    # ─────────────────────────────

    "navigation": [
        "take me",
        "go to",
        "where is",
        "navigate",
        "show direction",
        "guide me",
        "hospital direction"
    ],


    # ─────────────────────────────
    # ICU NAVIGATION
    # ─────────────────────────────

    "icu_navigation": [
        "where is icu",
        "icu",
        "take me to icu",
        "icu location",
        "how to go to icu"
    ],


    # ─────────────────────────────
    # OPD NAVIGATION
    # ─────────────────────────────

    "opd_navigation": [
        "where is opd",
        "opd",
        "take me to opd",
        "opd location"
    ],


    # ─────────────────────────────
    # PHARMACY NAVIGATION
    # ─────────────────────────────

    "pharmacy_navigation": [
        "where is pharmacy",
        "pharmacy",
        "medicine shop",
        "medical store",
        "take me to pharmacy"
    ],


    # ─────────────────────────────
    # RECEPTION NAVIGATION
    # ─────────────────────────────

    "reception_navigation": [
        "where is reception",
        "reception",
        "front desk",
        "help desk"
    ],


    # ─────────────────────────────
    # WASHROOM NAVIGATION
    # ─────────────────────────────

    "washroom_navigation": [
        "where is washroom",
        "washroom",
        "toilet",
        "restroom",
        "bathroom"
    ],


    # ─────────────────────────────
    # EMERGENCY WARD NAVIGATION
    # ─────────────────────────────

    "emergency_navigation": [
        "where is emergency ward",
        "emergency ward",
        "emergency room",
        "casualty ward"
    ],


    # ─────────────────────────────
    # MOVEMENT
    # ─────────────────────────────

    "move_forward": [
        "move forward",
        "go forward",
        "forward",
        "can you move forward",
        "move ahead"
    ],

    "move_backward": [
        "move backward",
        "go backward",
        "backward",
        "reverse",
        "move back"
    ],

    "move_left": [
        "turn left",
        "go left",
        "move left"
    ],

    "move_right": [
        "turn right",
        "go right",
        "move right"
    ],

    "move_stop": [
        "stop",
        "halt",
        "freeze",
        "stop moving"
    ],


    # ─────────────────────────────
    # SPO2 + BPM
    # ─────────────────────────────

    "spo2_check": [
        "check spo2",
        "check oxygen",
        "oxygen level",
        "measure oxygen",
        "check blood oxygen",
        "spo2",
        "oxygen test",
        "check pulse",
        "heart rate",
        "check bpm",
        "measure heart rate",
        "measure pulse"
    ],


    # ─────────────────────────────
    # TEMPERATURE
    # ─────────────────────────────

    "temperature_check": [
        "check temperature",
        "body temperature",
        "measure temperature",
        "fever check"
    ],


    # ─────────────────────────────
    # NURSE CALL
    # ─────────────────────────────

    "call_nurse": [
        "call nurse",
        "need nurse",
        "nurse please",
        "can you call nurse"
    ],


    # ─────────────────────────────
    # WATER / FOOD HELP
    # ─────────────────────────────

    "patient_help": [
        "i need water",
        "need food",
        "hungry",
        "thirsty",
        "need assistance"
    ],


    # ─────────────────────────────
    # EXIT
    # ─────────────────────────────

    "exit": [
        "shutdown",
        "shut down",
        "stop system",
        "power off",
        "turn off"
    ]
}

# 🔥 Priority commands (instant trigger)
PRIORITY = ["emergency", "help", "stop"]


# 🔥 Preprocess
def preprocess(text):
    return text.lower().strip()

# 🔥 RULE-BASED (FAST + CRITICAL)
def rule_based(text):
    for intent, keywords in INTENTS.items():
        for word in keywords:
            if word in text:
                if len(word) > 3:
                    return intent
    return None

# 🔥 NLP SIMILARITY
def similarity_match(text):
    doc = nlp(text)
    best_intent = None
    best_score = 0

    for intent, examples in INTENTS.items():
        for example in examples:
            score = doc.similarity(nlp(example))
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score > 0.75:
        return best_intent
    return "unknown"

def detect_intent(text):
    text = text.lower().strip()

    # 🔥 STRICT EXIT CONDITION
    if "shutdown" in text or "shut down" in text:
        return "exit"

    if "help" in text or "emergency" in text:
        return "emergency"

    if "time" in text:
        return "time_query"

    if "spo2" in text or "oxygen" in text:
        return "spo2_check"

    # ICU

    if "icu" in text:
        return "icu_navigation"


    # EMERGENCY

    if "emergency ward" in text:
        return "emergency_navigation"


    # OPD

    if "opd" in text:
        return "opd_navigation"


    # RECEPTION

    if "reception" in text:
        return "reception_navigation"


    # PHARMACY

    if "pharmacy" in text or "medicine" in text:
        return "pharmacy_navigation"


    # WASHROOM

    if "washroom" in text or "toilet" in text:
        return "washroom_navigation"

    if "hello" in text or "hi" in text or "hey" in text:
        return "greeting"

    # 🔥 THANK YOU FIX
    if "thank" in text or "thanks" in text:
        return "thanks"

    if "forward" in text:
        return "move_forward"
    if "backward" in text or "reverse" in text or "back" in text:
        return "move_backward"
    if "left" in text:
        return "move_left"
    if "right" in text:
        return "move_right"
    if "stop" in text or "halt" in text:
        return "move_stop"


    # 🔥 EXIT SAFETY
    if "shutdown" in text:
        return "exit"

    return "unknown"
