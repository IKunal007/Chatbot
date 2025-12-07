from pathlib import Path
from datetime import datetime

def export_chat(history, filename=None):
    """
    Export the chat history to a text file in a clean, readable format.
    """

    export_dir =  Path("data")
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = export_dir/f"chat_export_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== Chat Transcript ===\n\n")

        for turn in history:
            user_msg = turn["User_text"]
            bot_msg = turn["Bot_reply"]
            sentiment = turn["label"]
            score = turn["score"]

            f.write(f"User: {user_msg}\n")
            f.write(f"Sentiment: {sentiment} (compound={score})\n")
            f.write(f"Bot: {bot_msg}\n")
            f.write("-" * 40 + "\n")

    print(f"Chat exported successfully: {filename}")
