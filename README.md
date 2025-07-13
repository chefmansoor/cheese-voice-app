# Cheese Voice Inventory App

A voice-first inventory logger built with Streamlit, OpenAI GPT, Whisper, and Google Sheets.

## Deploy on Streamlit

1. Upload this project to a private GitHub repo.
2. Go to https://streamlit.io/cloud and create a new app.
3. Set the file path to `cheese_voice_inventory_app.py`.
4. Add the following secrets under Settings > Secrets:

```toml
OPENAI_API_KEY = "your-openai-api-key"
GOOGLE_SHEET_ID = "your-google-sheet-id"
GOOGLE_CREDS_BASE64 = "base64-encoded-google-creds"
```

5. Run the app in Chrome. Click to record your inventory input.

