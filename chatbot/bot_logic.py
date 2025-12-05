import json
import random
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        with open(self.intents_path, 'r') as f:
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
