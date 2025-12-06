# pages/1_Conversation_Analysis.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # altair import not needed now

from chatbot.sentiment import analyze_trend, summarize_conversation


def plot_simple_sentiment_graph(history):
    # Use VADER compound scores as intensity
    scores = [h["score"] for h in history]
    msg_numbers = list(range(1, len(scores) + 1))

    fig, ax = plt.subplots(figsize=(10, 4))

    # Line of intensity over time
    ax.plot(msg_numbers, scores, marker="o", linewidth=2)

    # Zero (neutral) reference line
    ax.axhline(0, color="gray", linewidth=1, linestyle="--", alpha=0.7)

    # Limit to [-1, 1] which is VADER's natural range
    ax.set_ylim(-1, 1)

    # Show categories as tick labels, but keep intensity in between
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["Negative", "Neutral", "Positive"], fontsize=12)

    ax.set_xlabel("Message Number", fontsize=12)
    ax.set_ylabel("Sentiment (intensity)", fontsize=12)
    ax.set_title("Sentiment Trend Over Conversation", fontsize=15)

    ax.grid(True, linestyle="--", alpha=0.3)

    return fig


def main():
    st.title("Conversation Analysis")

    # All completed chats stored by your app
    chats = st.session_state.get("chats", [])
    current_history = st.session_state.get("history", [])
    finished_current = st.session_state.get("finished", False)

    # --------- Choose which conversation to analyze ---------
    history = None
    overall_label = None
    trend_text = None

    if chats:
        st.subheader("Select conversation")

        # remember last selected chat, default to latest
        if "analysis_selected_chat_index" not in st.session_state:
            st.session_state.analysis_selected_chat_index = len(chats) - 1

        idx = st.selectbox(
            "Choose a chat:",
            options=list(range(len(chats))),
            index=st.session_state.analysis_selected_chat_index,
            format_func=lambda i: f"Chat {i + 1}",
        )
        st.session_state.analysis_selected_chat_index = idx

        selected = chats[idx]
        history = selected["history"]
        overall_label = selected.get("overall")
        trend_text = selected.get("trend")
        finished = True  # saved chats are always finished
    else:
        # Fallback: no saved chats yet, use current ongoing one
        history = current_history
        finished = finished_current

    if not history:
        st.info(
            "No conversation history yet. Go to the main Chat page and start "
            "talking to the bot. Once you end a chat with `/quit`, `quit`, or "
            "`exit`, it will appear here."
        )
        return

    # --------- Overall summary ---------
    st.subheader("Overall Sentiment")

    # If we don't have cached values (e.g. current ongoing chat), recompute
    if overall_label is None:
        overall_label = summarize_conversation(history)
    if trend_text is None:
        scores = [h["score"] for h in history]
        trend_text = analyze_trend(scores)

    st.markdown(f"**Overall conversation sentiment:** {overall_label}")
    st.markdown(f"**Mood trend:** {trend_text}")

    if not finished:
        st.caption(
            "Note: Conversation is still ongoing. Summary will update as more "
            "messages are added."
        )

    st.markdown("---")

    # --------- Build dataframe once (for table) ---------
    rows = [
        {
            "Message #": i + 1,
            "User message": h["User_text"],
            "User sentiment": h["label"],
            "Sentiment score": round(h["score"], 3),
            "Bot reply": h["Bot_reply"],
        }
        for i, h in enumerate(history)
    ]
    df = pd.DataFrame(rows)

    # --------- Simple categorical line graph ---------
    st.subheader("Sentiment Over Conversation")

    fig = plot_simple_sentiment_graph(history)
    st.pyplot(fig)

    st.caption(
        "This chart shows how the user's sentiment moves between Negative, Neutral, and Positive across the conversation."
    )

    st.markdown("---")

    # --------- Detailed table ---------
    st.subheader("Message-Level Sentiment")

    st.dataframe(df)

    st.markdown(
        "_This page uses the same sentiment scores as the chat page "
        "but presents them visually and in a structured table for easier review._"
    )


if __name__ == "__main__":
    main()
