
# Ares Chatbot

This chatbot maintains the full conversation history, performs per-message sentiment analysis, 
and at the end computes an overall sentiment and mood trend.

## How to Run

### Option 1
---

### Option 2

### 1. Clone the repository
```bash
git clone <https://github.com/IKunal007/Chatbot.git>
cd ChatBot
```

### 2. Create and activate a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```
macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

This will open the chatbot UI at:

http://localhost:8501

### 5. Ending a conversation

Computes full conversation sentiment

Analyzes mood trend

Stores the chat under the Chat History page

Displays navigation buttons for analysis or starting a new chat

##  Chosen Technologies

### **Programming Language**
- **Python 3.9+**

---

### **Libraries Used**

| Library       | Purpose                                    |
|---------------|--------------------------------------------|
| Streamlit     | Web UI + multipage layout                  |
| scikit-learn  | TF-IDF vectorization + cosine similarity   |
| VADER         | Message-level sentiment scoring            |
| NLTK          | Tokenization and preprocessing             |
| Pandas        | Data table construction                    |
| Matplotlib    | Sentiment trend graph                      |
| pytest        | Unit testing                               |
| NumPy         | Numerical utilities                        |



##  How the Chatbot Works

### Retrieval-Based Chatbot (Bot Engine)

The chatbot uses a simple **TF-IDF + cosine similarity** method:

1. All patterns from `intents.json` are converted into TF-IDF vectors.
2. The user message is also vectorized.
3. Cosine similarity is computed between the message and all patterns.
4. If the best similarity score is below a confidence threshold, a fallback reply is used.
5. Otherwise, the bot returns a response linked to the most similar intent.

**Why this approach?**
- Fast and lightweight  
- Predictable responses  
- Easy to expand by editing `intents.json`  

**Core implementation:** `chatbot/bot_logic.py`


##  Sentiment Logic Explanation

The chatbot uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** as its primary sentiment analysis tool.  
VADER is well-suited for conversational text because it understands social-media style messages, slang, negations, punctuation emphasis, and even repeated characters.

The sentiment system works on two levels:  
1. **Each individual user message is analyzed immediately**, and  
2. **The overall emotional direction of the entire conversation is inferred** once the chat ends.


##  How Message Sentiment Is Determined

Whenever the user sends a message, VADER generates four values:

- **neg** — Degree of negativity  
- **neu** — Degree of neutrality  
- **pos** — Degree of positivity  
- **compound** — A single normalized score from **–1 (very negative)** to **+1 (very positive)**  

The **compound** score represents the overall emotional tone of the message.

The chatbot uses the recommended VADER thresholds for labeling:

```python
if compound >= 0.05:
    Positive
elif compound <= -0.05:
    Negative
else:
    Neutral
```

##  Tests

All **non-UI logic** is tested using **pytest**.

### Test Suite (located in `tests/`)

#### **1. `test_bot.py`**
- Verifies bot loads intents correctly  
- Checks TF-IDF vectorization + cosine similarity  
- Ensures fallback responses work as expected  

#### **2. `test_sentiment.py`**
- Tests message-level sentiment labeling (Positive / Neutral / Negative)  
- Tests conversation-level sentiment aggregation  
- Tests mood trend detection logic  


###  Running Tests

Use either command:

```bash
pytest
```

```bash
python -m pytest
```

These tests run entirely on backend logic and do not depend on Streamlit, ensuring fast and reliable testing of the core engine.        