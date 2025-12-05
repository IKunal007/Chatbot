from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

sia = SentimentIntensityAnalyzer()

def get_sentiment_label_and_score(text: str):
    s = sia.polarity_scores(text)
    compound = s["compound"]
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return label, compound


def score_to_label(score: float) -> str:
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_trend(history_scores):
    """
    history_scores: list of VADER compound scores (floats)
    Returns a human-readable trend description.
    """
    if len(history_scores) < 2:
        return "Not enough data to determine mood trend."

    start = history_scores[0]
    end = history_scores[-1]
    mid = history_scores[len(history_scores) // 2]

    start_label = score_to_label(start)
    mid_label = score_to_label(mid)
    end_label = score_to_label(end)

    if start_label == mid_label == end_label:
        return f"Tone remained consistently {start_label.lower()} throughout the conversation."

    trend = (
        f"Conversation started {start_label.lower()}, "
        f"shifted to {mid_label.lower()} midway, "
        f"and ended {end_label.lower()}."
    )
    return trend


