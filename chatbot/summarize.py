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
