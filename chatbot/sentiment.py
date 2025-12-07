from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
    if len(history_scores) < 2:
        return "Not enough data to determine mood trend."

    # Convert scores → labels
    labels = [score_to_label(s) for s in history_scores]

    start = labels[0]
    end = labels[-1]

    # Count transitions (e.g., Positive→Neutral→Negative)
    transitions = sum(
        1 for i in range(1, len(labels)) if labels[i] != labels[i - 1]
    )

    # --- 1. Completely constant tone (already handled but improved) ---
    if len(set(labels)) == 1:
        return f"Tone remained consistently {start.lower()} throughout the conversation."

    # --- 2. Clear improvement (Negative → Neutral/Positive) ---
    if start == "Negative" and end == "Positive":
        return "Tone improved significantly — conversation moved from negative to positive."

    if start == "Negative" and end == "Neutral":
        return "Tone improved slightly — started negative but recovered to neutral."

    # --- 3. Clear decline (Positive → Neutral/Negative) ---
    if start == "Positive" and end == "Negative":
        return "Tone declined significantly — conversation turned from positive to negative."

    if start == "Positive" and end == "Neutral":
        return "Tone became less positive — conversation softened to neutral."

    # --- 4. Up–down fluctuations (3+ transitions) ---
    if transitions >= 3:
        return "Tone fluctuated frequently with mixed emotional shifts."

    # --- 5. Simple 1-step shift (most common case) ---
    if start != end and transitions == 1:
        return f"Tone shifted from {start.lower()} to {end.lower()}."

    # --- 6. Two-phase conversation (start → mid → end) ---
    mid_label = labels[len(labels) // 2]

    if start != mid_label or mid_label != end:
        return (
            f"Conversation started {start.lower()}, "
            f"shifted to {mid_label.lower()} midway, "
            f"and ended {end.lower()}."
        )

    # fallback
    return "Mood trend shows mixed shifts over time."


def summarize_conversation(history):

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

    # determine overall label from weighted score
    if weighted_score >= 0.05:
        overall = "Positive"
    elif weighted_score <= -0.05:
        overall = "Negative"
    else:
        overall = "Neutral"

    return overall

