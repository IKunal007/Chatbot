# pages/3_History.py
import streamlit as st
import json


def main():
    st.title("Conversation History (Current Session)")

    chats = st.session_state.get("chats", [])

    if not chats:
        st.info("No completed chats yet. End a conversation using `/quit`, `quit`, or `exit` to add it here.")
        return

    st.subheader("Select a conversation to view")

    chat_index = st.selectbox(
        "Choose a chat:",
        options=list(range(len(chats))),
        format_func=lambda i: f"Chat {i + 1}",
    )

    selected = chats[chat_index]

    st.markdown("---")
    st.subheader(f"Chat {chat_index + 1} Summary")

    st.markdown(f"**Overall Sentiment:** {selected['overall']}")
    st.markdown(f"**Mood Trend:** {selected['trend']}")
    st.markdown("---")

    st.subheader("Full Conversation")

    for turn in selected["history"]:
        with st.chat_message("user"):
            st.markdown(turn["User_text"])
            st.markdown(f"_Sentiment: **{turn['label']}**_")

        with st.chat_message("assistant"):
            st.markdown(turn["Bot_reply"])

    st.markdown("---")
    st.subheader("Download This Conversation")

    st.download_button(
        label="Download Chat as TXT",
        data=selected["export_text"],
        file_name=f"chat_{chat_index + 1}.txt",
        mime="text/plain",
    )


if __name__ == "__main__":
    main()
