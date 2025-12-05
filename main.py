from pathlib import Path

from chatbot.bot_logic import SimpleRetrievalBot
from chatbot.sentiment import get_sentiment_label_and_score, analyze_trend
from chatbot.history import save_history
from chatbot.export_chat import export_chat
from chatbot.summarize import summarize_conversation

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INTENTS_PATH = Path("intents.json")

def main():
    # Sentiment setup
    sia = SentimentIntensityAnalyzer()

    # Bot setup
    bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.3)

    # Conversation history
    history = []  # list of {"text":..., "label":..., "score":..., "Bot_reply":...}

    print("Chatbot ready. Type '/quit' to exit.\n")
    while True:
        user = input("User: ").strip()
        if user.lower() in ("/quit", "quit", "exit"):
            break

        # Per-message sentiment
        sentiment_label, compound = get_sentiment_label_and_score(user)
        print(f"→ Sentiment: {sentiment_label} ")

        # Get bot reply
        reply = bot.reply(user)
        print(f"Bot: {reply}\n")

        history.append({"User_text": user, "label": sentiment_label, "score": compound,"Bot_reply": reply})

    overall_label = summarize_conversation(history)

    print("\n----- Conversation summary -----")

    print("\nFinal Output:")
    print(f"Overall conversation sentiment: {overall_label}")

    score = [h["score"] for h in history]
    trend = analyze_trend(score)
    print(f"Mood trend: {trend}")

    save_history(history)
    export_chat(history)

if __name__ == "__main__":
    main()
