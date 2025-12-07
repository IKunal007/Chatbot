import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import aggregate_overall_sentiment


def test_aggregate_positive():
    scores = [0.2, 0.4, 0.1]  # positive
    label, mean = aggregate_overall_sentiment(scores)
    assert label == "Positive"
    assert mean > 0


def test_aggregate_negative():
    scores = [-0.3, -0.6, -0.2]  # negative
    label, mean = aggregate_overall_sentiment(scores)
    assert label == "Negative"
    assert mean < 0


def test_aggregate_neutral_empty_history():
    scores = []
    label, mean = aggregate_overall_sentiment(scores)
    assert label == "Neutral"
    assert mean == 0.0


def test_aggregate_neutral_mixed():
    scores = [0.1, -0.1, 0.0]  # roughly cancels out
    label, mean = aggregate_overall_sentiment(scores)
    assert label == "Neutral"
