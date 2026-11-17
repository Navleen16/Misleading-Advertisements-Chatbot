# AdAlert – Streamlit Gemini Chatbot

A Streamlit version of the supplied knowledge-based AdAlert chatbot.

## 1. Requirements
- Python 3.10 or newer
- A Gemini API key

## 2. Install dependencies
Open a terminal in this project folder and run:

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
.venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## 3. Configure the API key
Open `.streamlit/secrets.toml` and replace:

```toml
GEMINI_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
```

with your own Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"
GEMINI_MODEL = "gemini-3.5-flash-lite"
```

If that model is not available for your API key, change `GEMINI_MODEL` to a model currently enabled for your Google AI Studio account.

**Security:** Do not share your real API key, commit `secrets.toml` to Git, or upload it publicly. The included file contains only a placeholder.

## 4. Run the app

```bash
streamlit run app.py
```

Streamlit will display a local URL (usually `http://localhost:8501`) to open in your browser.

## Features
- Chat-style Streamlit interface
- Gemini-powered answers
- Knowledge manual embedded in the app
- Short conversation history for follow-up questions
- Clear chat button
- API key read from `.streamlit/secrets.toml`
- Basic error handling for configuration and API errors

## Important note
The chatbot is an educational information tool, not a lawyer or an official government service. The supplied knowledge manual is used as its reference material. Verify current legal requirements and complaint procedures through official sources.
