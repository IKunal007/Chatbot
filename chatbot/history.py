import json

def save_history(history, filename="history.json"):
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)
