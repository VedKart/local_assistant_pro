from dataclasses import dataclass

@dataclass
class Persona:
    name: str = "Локальный ассистент"
    style: str = "Дружелюбный, вежливый, лаконичный"
    tts_voice: str = "xenia"
    base_prompt: str = (
        "Ты — локальный русскоязычный ассистент, работающий офлайн. Отвечай кратко и по делу."
    )

EMOTION_WORDS = {
    "angry": ["злю", "бес", "раздраж", "зол", "бесит"],
    "sad": ["печал", "груст", "жаль", "обидно"],
    "happy": ["класс", "супер", "спасибо", "рад", "отлично"],
    "neutral": [],
}

persona = Persona()

def detect_emotion(text: str) -> str:
    t = text.lower()
    for k, words in EMOTION_WORDS.items():
        if any(w in t for w in words):
            return k
    if "!" in t and "?" not in t:
        return "happy"
    if ":(" in t:
        return "sad"
    return "neutral"

def build_system_prompt(kb_context: str, user_msg: str) -> str:
    emo = detect_emotion(user_msg)
    emo_instruction = {
        "angry": "Собеседник раздражён — держи спокойный, поддерживающий тон.",
        "sad": "Собеседник расстроен — отвечай бережно.",
        "happy": "Собеседник рад — поддержи позитив.",
        "neutral": "Нейтральный тон.",
    }[emo]
    base = f"Персона: {persona.name}. Стиль: {persona.style}. {emo_instruction}\n\n" + persona.base_prompt
    if kb_context:
        base += "\n\nКонтекст (может быть нерелевантным):\n" + kb_context
    return base
