# main.py
import json
import random
from pathlib import Path

import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INTENTS_PATH = Path("intents.json")

class SimpleRetrievalBot:
    def __init__(self, intents_path: Path, min_confidence=0.3):
        self.intents_path = intents_path
        self.min_confidence = min_confidence
        self.pattern_texts = []           # list of pattern strings
        self.pattern_to_tag = []          # parallel list of tags
        self.tag_to_responses = {}        # map tag -> [responses]
        self.vectorizer = None
        self.tfidf = None
        self._load_intents()

    def _load_intents(self):
        with open(self.intents_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for intent in data.get("intents", []):
            tag = intent["tag"]
            responses = intent.get("responses", [])
            patterns = intent.get("patterns", [])
            self.tag_to_responses[tag] = responses
            for p in patterns:
                self.pattern_texts.append(p)
                self.pattern_to_tag.append(tag)
        # build TF-IDF index
        self.vectorizer = TfidfVectorizer(lowercase=True, token_pattern=r"(?u)\b\w+\b")
        self.tfidf = self.vectorizer.fit_transform(self.pattern_texts)

    def reply(self, user_text: str):
        if not user_text.strip():
            return "Please say something."

        user_vec = self.vectorizer.transform([user_text])
        sims = cosine_similarity(user_vec, self.tfidf)[0]  # shape (n_patterns,)
        best_idx = int(sims.argmax())
        best_score = float(sims[best_idx])
        best_tag = self.pattern_to_tag[best_idx]

        if best_score < self.min_confidence:
            # fallback reply
            return random.choice([
                "Sorry, I didn't understand. Could you rephrase?",
                "I'm not sure I follow — can you tell me more?"
            ])
        return random.choice(self.tag_to_responses.get(best_tag, ["Sorry."]))


def aggregate_overall_sentiment(history_scores):
    # history_scores: list of float compound scores from VADER
    if not history_scores:
        return "Neutral", 0.0
    mean = sum(history_scores) / len(history_scores)
    if mean >= 0.05:
        label = "Positive"
    elif mean <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return label, mean

def main():
    # Sentiment setup
    sia = SentimentIntensityAnalyzer()

    # Bot setup
    bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.3)

    # Conversation history
    history = []  # list of {"text":..., "label":..., "score":...}

    print("Chatbot ready. Type '/quit' to exit.\n")
    while True:
        user = input("User: ").strip()
        if user.lower() in ("/quit", "quit", "exit"):
            break

        # Per-message sentiment
        s = sia.polarity_scores(user)
        compound = s["compound"]
        if compound >= 0.05:
            sentiment_label = "Positive"
        elif compound <= -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        print(f"→ Sentiment: {sentiment_label} (compound={compound:.3f})")

        # Get bot reply
        reply = bot.reply(user)
        print(f"Bot: {reply}\n")

        history.append({"text": user, "label": sentiment_label, "score": compound})

    overall_label, overall_score = aggregate_overall_sentiment([h["score"] for h in history])
    print("\n----- Conversation summary -----")
    print(f"Overall conversation sentiment: {overall_label} (mean_compound={overall_score:.3f})")
    # optional: short rationale
    if overall_label == "Positive":
        print("Rationale: Conversation leans positive.")
    elif overall_label == "Negative":
        print("Rationale: Conversation leans negative — user showed dissatisfaction.")
    else:
        print("Rationale: Mixed or neutral sentiment across messages.")

if __name__ == "__main__":
    main()
