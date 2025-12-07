# app.py
from pathlib import Path

import streamlit as st

from chatbot.bot_logic import SimpleRetrievalBot
from chatbot.sentiment import (
    get_sentiment_label_and_score,
    analyze_trend,
    summarize_conversation,
)

INTENTS_PATH = Path("intents.json")
QUIT_COMMANDS = ("/quit", "quit", "exit")


def init_state():
    if "bot" not in st.session_state:
        st.session_state.bot = SimpleRetrievalBot(INTENTS_PATH, min_confidence=0.3)

    if "history" not in st.session_state:
        # list of {"User_text", "Bot_reply", "label", "score"}
        st.session_state.history = []

    if "finished" not in st.session_state:
        st.session_state.finished = False

    if "overall_label" not in st.session_state:
        st.session_state.overall_label = None

    if "trend" not in st.session_state:
        st.session_state.trend = None

    if "chats" not in st.session_state:
        st.session_state.chats = []


def end_conversation():
    """Compute summary, mood trend, store in session, and mark finished."""
    history = st.session_state.history

    if not history:
        overall = "Neutral"
        trend = "No messages to analyze."
        export_text = "No chat available."
    else:
        overall = summarize_conversation(history)
        scores = [h["score"] for h in history]
        trend = analyze_trend(scores)
        export_text = "\n".join(
            [
                f"User: {h['User_text']}\n"
                f"Sentiment: {h['label']}\n"
                f"Bot: {h['Bot_reply']}\n"
                for h in history
            ]
        )

    # make sure chats list exists
    if "chats" not in st.session_state:
        st.session_state.chats = []

    # store this chat in memory only
    st.session_state.chats.append(
        {
            "history": history.copy(),
            "overall": overall,
            "trend": trend,
            "export_text": export_text,
        }
    )

    # Build final one-line conclusion
    if overall == "Positive":
        conclusion = "General satisfaction"
    elif overall == "Negative":
        conclusion = "General dissatisfactoin."
    else:
        conclusion = "Balanced emotional tone."

    st.session_state.conclusion = conclusion
    st.session_state.overall_label = overall
    st.session_state.trend = trend
    st.session_state.finished = True



def main():
    st.set_page_config(page_title="Sentiment Chatbot", page_icon="💬")
    init_state()

    bot = st.session_state.bot
    history = st.session_state.history
    finished = st.session_state.finished

    # ---------- SECTION 1: HEADER (title + description) ----------
    st.title("Ares Chatbot")

    st.markdown(
        "This chatbot maintains the full conversation history, "
        "performs **per-message sentiment analysis**, and at the end "
        "computes an **overall sentiment** and **mood trend**."
    )

    st.divider()

    # ---------- SECTION 2: MAIN CONTENT (chat) ----------
    if finished:
        # Conversation ended → show summary only (no full chat)
        st.subheader("Conversation Summary")
        st.success("The conversation has ended.")

        st.markdown(
            f"**Overall conversation sentiment:** {st.session_state.overall_label} - {st.session_state.conclusion}"
        )
        st.markdown(f"**Mood trend:** {st.session_state.trend}")
        st.markdown(
            "_Chat history has been saved_"
        )
    else:
        # Conversation ongoing → show chat + input
        # Chat history (bubbles)
        if not history:
            with st.chat_message("assistant"):
                st.markdown("Hi! I'm your sentiment-aware chatbot. How can I help you today?")
        else:
            for turn in history:
                with st.chat_message("user"):
                    st.markdown(turn["User_text"])
                    st.markdown(f"_Sentiment: **{turn['label']}**_")

                with st.chat_message("assistant"):
                    st.markdown(turn["Bot_reply"])

        # Input at bottom – Enter sends message
        user_input = st.chat_input("Type your message")

        if user_input and user_input.strip():
            text = user_input.strip()
            lower = text.lower()

            # exit commands (end loop)
            if lower in QUIT_COMMANDS:
                end_conversation()
            else:
                sentiment_label, compound = get_sentiment_label_and_score(text)
                bot_reply = bot.reply(text)

                history.append(
                    {
                        "User_text": text,
                        "Bot_reply": bot_reply,
                        "label": sentiment_label,
                        "score": compound,
                    }
                )
                st.session_state.history = history

            st.rerun()

    st.divider()

    # ---------- SECTION 3: ACTION BUTTONS / FOOTER ----------
    if finished:
        st.subheader("What would you like to do next?")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.page_link(
                "pages/1_Conversation_Analysis.py",
                label="📈 Conversation Analysis",
            )

        with col2:
            st.page_link(
                "pages/2_History.py",
                label="🕒 Chat History",
            )

        with col3:
            if st.button("🔄 Start New Conversation"):
                # reset everything except bot instance
                st.session_state.history = []
                st.session_state.finished = False
                st.session_state.overall_label = None
                st.session_state.trend = None
                st.session_state.export_done = False
                st.rerun()
    else:
        st.markdown(
        "_To end the conversation type_ `/quit`, `quit` _or_ `exit` "
        )

        st.caption("Type your message below and press Enter to chat with the bot.")

if __name__ == "__main__":
    main()
