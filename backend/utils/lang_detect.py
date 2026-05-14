import re
try:
    from langdetect import detect
except ImportError:
    detect = None

HINGLISH_PATTERNS = [
    r"\b(kya|hai|mein|karo|batao|samjhao|bolo|hota|kaise|yaar|bhai|aur|nahi|dekho|isko|uska|ye|woh|toh|phir|ab|sab|bahut)\b",
    r"\b(mitosis|cell|dna|rna|photosynthesis)\s+(kya|ka|ki|ke|mein|hai)",
]
URDU_SCRIPT = re.compile(r"[\u0600-\u06FF]")
HINDI_SCRIPT = re.compile(r"[\u0900-\u097F]")


def detect_language(text: str) -> str:
    if URDU_SCRIPT.search(text):
        return "ur"
    if HINDI_SCRIPT.search(text):
        return "hi"
    for pattern in HINGLISH_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "hinglish"
    if detect:
        try:
            detected = detect(text)
            if detected == "hi":
                return "hi"
            if detected == "ur":
                return "ur"
        except Exception:
            pass
    return "en"
