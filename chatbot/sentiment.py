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

def summarize_conversation(history):
    """
    history: list of dicts with at least a 'score' key (VADER compound)
    returns: overall_label, rationale_text
    """
    scores = [h["score"] for h in history]
    if not scores:
        return "Neutral", "no messages to analyze."

    # weights based on strength of each message
    weights = [abs(s) for s in scores]
    total_weight = sum(weights)

    if total_weight == 0:
        # all scores are 0 → perfectly neutral chat
        return "Neutral", "conversation was emotionally flat / neutral."

    # weighted sentiment: strong emotions count more
    weighted_score = sum(s * w for s, w in zip(scores, weights)) / total_weight

    # emotional intensity (how strong feelings were overall)
    avg_intensity = total_weight / len(scores)

    # determine overall label from weighted score
    if weighted_score >= 0.05:
        overall = "Positive"
    elif weighted_score <= -0.05:
        overall = "Negative"
    else:
        overall = "Neutral"

    # build rationale
    if avg_intensity < 0.2:
        intensity_desc = "low emotional intensity"
    elif avg_intensity < 0.5:
        intensity_desc = "moderate emotional intensity"
    else:
        intensity_desc = "high emotional intensity"


    return overall

