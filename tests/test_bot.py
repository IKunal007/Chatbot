import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SimpleRetrievalBot, INTENTS_PATH


def test_bot_reply_is_string():
    bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.0)
    reply = bot.reply("hello")
    assert isinstance(reply, str)
    assert len(reply.strip()) > 0


def test_bot_fallback_for_nonsense():
    bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.99)
    # Very high min_confidence forces fallback most of the time
    reply = bot.reply("sdlkfjsldkfjsldkfjsldkfj")
    text = reply.lower()
    # Must contain some hint of fallback
    assert ("sorry" in text) or ("not sure" in text)
