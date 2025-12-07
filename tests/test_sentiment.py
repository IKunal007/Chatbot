from chatbot.sentiment import (
    get_sentiment_label_and_score,
    summarize_conversation,
    analyze_trend,
)


def test_get_sentiment_label_and_score_positive():
    label, score = get_sentiment_label_and_score("I really love this, it's great!")
    assert label == "Positive"
    assert score > 0


def test_get_sentiment_label_and_score_negative():
    label, score = get_sentiment_label_and_score("This is terrible and I hate it.")
    assert label == "Negative"
    assert score < 0


def test_summarize_conversation_positive_overall():
    history = [
        {"score": 0.6},
        {"score": 0.4},
        {"score": 0.5},
    ]
    overall = summarize_conversation(history)
    assert overall == "Positive"


def test_summarize_conversation_negative_overall():
    history = [
        {"score": -0.6},
        {"score": -0.4},
        {"score": -0.5},
    ]
    overall = summarize_conversation(history)
    assert overall == "Negative"


def test_analyze_trend_improves():
    scores = [-0.4, -0.1, 0.2, 0.5]
    trend = analyze_trend(scores)
    # Just check it mentions "improved" or "positive"
    assert "improved" in trend or "positive" in trend.lower()
