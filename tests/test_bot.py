from pathlib import Path
from chatbot.bot_logic import SimpleRetrievalBot

INTENTS_PATH = Path("intents.json")


def test_bot_reply_is_string():
    bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.0)
    reply = bot.reply("hello")

    assert isinstance(reply, str)
    assert reply.strip() != ""


def test_bot_fallback_for_nonsense():
    bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.99)

    reply = bot.reply("sdlfkjsdlfkjweoiruwoeiur")
    text = reply.lower()

    assert ("sorry" in text) or ("not sure" in text)
