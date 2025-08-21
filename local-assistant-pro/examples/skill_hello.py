from local_assistant_pro.skills.base import Skill

class HelloSkill(Skill):
    name = "hello"
    def on_request(self, user_text: str, context: dict) -> str | None:
        if user_text.lower().startswith("привет"):
            return "Привет! Я плагин. Чем помочь?"
        return None
